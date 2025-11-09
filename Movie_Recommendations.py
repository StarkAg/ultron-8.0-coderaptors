import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
from ast import literal_eval
import warnings
import os
warnings.filterwarnings('ignore')

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(SCRIPT_DIR, 'datasets')

# Read CSV files with proper path handling
df1 = pd.read_csv(os.path.join(DATASETS_DIR, 'tmdb_5000_credits.csv'))
df2 = pd.read_csv(os.path.join(DATASETS_DIR, 'tmdb_5000_movies.csv'))

df1.columns = ['id','title_x','cast','crew']
df2 = df2.merge(df1,on = 'id')
df2.head(5)

m = df2['vote_count'].quantile(0.9)
C = df2['vote_average'].mean()

def weight_average(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m))*R + (m/(v+m))*C

q_movies = df2.copy().loc[df2['vote_count'] >= m]
q_movies['score'] = q_movies.apply(weight_average , axis = 1)
q_movies = q_movies.sort_values('score' , ascending = False)

tfidf = TfidfVectorizer( stop_words='english' )
df2['overview'] = df2['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(df2['overview'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

def get_recommendations(title,cosine_sim = cosine_sim):
    # Case-insensitive search with fuzzy matching
    title_lower = title.lower().strip()
    
    # Try exact match first
    if title in indices:
        idx = indices[title]
    else:
        # Try case-insensitive match
        matching_titles = df2[df2['title'].str.lower() == title_lower]
        if len(matching_titles) > 0:
            idx = matching_titles.index[0]
        else:
            # Try partial/fuzzy match
            matching_titles = df2[df2['title'].str.lower().str.contains(title_lower, na=False)]
            if len(matching_titles) > 0:
                idx = matching_titles.index[0]
            else:
                raise ValueError(f"Movie '{title}' not found in database. Please check the spelling or try a different movie.")
    
    # Get the source movie's genres for filtering
    source_movie = df2.iloc[idx]
    source_genres = set()
    if isinstance(source_movie.get('genres'), list):
        source_genres = set([g.lower() if isinstance(g, str) else str(g).lower() for g in source_movie.get('genres', [])])
    elif isinstance(source_movie.get('genres'), str):
        try:
            from ast import literal_eval
            genres_list = literal_eval(source_movie.get('genres', '[]'))
            source_genres = set([g.get('name', '').lower() if isinstance(g, dict) else str(g).lower() for g in genres_list])
        except:
            pass
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get more candidates and filter by genre similarity
    candidates = sim_scores[1:31]  # Get top 30 candidates for better filtering
    filtered_movies = []
    
    for score_idx, score in candidates:
        movie = df2.iloc[score_idx]
        movie_genres = set()
        
        # Extract genres
        if isinstance(movie.get('genres'), list):
            movie_genres = set([g.lower() if isinstance(g, str) else str(g).lower() for g in movie.get('genres', [])])
        elif isinstance(movie.get('genres'), str):
            try:
                from ast import literal_eval
                genres_list = literal_eval(movie.get('genres', '[]'))
                movie_genres = set([g.get('name', '').lower() if isinstance(g, dict) else str(g).lower() for g in genres_list])
            except:
                pass
        
        # Calculate genre overlap score
        if source_genres and movie_genres:
            genre_overlap_count = len(source_genres & movie_genres)
            genre_overlap_ratio = genre_overlap_count / max(len(source_genres), len(movie_genres))
            
            # Define action/sci-fi genres that should match well
            action_sci_fi_genres = {'action', 'adventure', 'sciencefiction', 'sci-fi', 'science fiction', 'thriller', 'crime'}
            source_is_action_sci_fi = len(source_genres & action_sci_fi_genres) > 0
            movie_is_action_sci_fi = len(movie_genres & action_sci_fi_genres) > 0
            
            # Exclude children/family/horror/fantasy for action movies
            exclude_genres = {'family', 'children', 'animation', 'horror', 'fantasy'}
            movie_has_excluded = len(movie_genres & exclude_genres) > 0
            
            # STRICT: Exclude family/children/horror/fantasy movies for action/sci-fi films
            # unless they have very high similarity (>0.4) AND multiple genre matches
            if source_is_action_sci_fi and movie_has_excluded and not movie_is_action_sci_fi:
                # Only allow if it's a sequel (high title similarity) with very high score
                if title_similarity < 0.3 or score < 0.4:
                    has_good_overlap = False  # Exclude children/family/horror movies for action films
                else:
                    has_good_overlap = genre_overlap_count >= 2 and score > 0.4
            elif source_is_action_sci_fi and movie_is_action_sci_fi:
                # For action movies, require at least 1 genre match
                # If 2+ genres match, require score > 0.08
                # If only 1 genre match, require score > 0.09 (excludes Cave Bear at 0.081)
                if genre_overlap_count >= 2:
                    has_good_overlap = score > 0.08  # Lower threshold for 2+ genres
                else:
                    has_good_overlap = score > 0.09  # Higher threshold for single genre (excludes 0.081)
            else:
                # For non-action movies, require 2+ genres OR high overlap ratio
                has_good_overlap = (genre_overlap_count >= 2 or genre_overlap_ratio > 0.6) and score > 0.25
        else:
            # If genre info is missing, rely on similarity score (must be high)
            has_good_overlap = score > 0.3 if source_genres or movie_genres else True
        
        # Also check if it's a sequel/same franchise (contains similar words)
        source_title_words = set(title.lower().split())
        movie_title = str(movie.get('title', '')).lower()
        movie_title_words = set(movie_title.split())
        title_similarity = len(source_title_words & movie_title_words) / max(len(source_title_words), 1)
        
        # Prioritize movies with title similarity or good genre overlap
        # For sequels (high title similarity), be more lenient
        # ONLY add if has_good_overlap is True (not False)
        if has_good_overlap:
            if title_similarity > 0.3:
                filtered_movies.append((score_idx, score, genre_overlap_count if source_genres and movie_genres else 0, title_similarity))
            else:
                filtered_movies.append((score_idx, score, genre_overlap_count if source_genres and movie_genres else 0, title_similarity))
        
        # Stop when we have 10 good recommendations
        if len(filtered_movies) >= 10:
            break
    
    # Sort by genre overlap and similarity, then take top 10
    filtered_movies.sort(key=lambda x: (x[2], x[3], x[1]), reverse=True)
    
    # If we don't have 10 after filtering, add more from similarity scores
    # BUT only add movies that pass basic filters (no excluded genres)
    if len(filtered_movies) < 10:
        remaining = []
        for x in candidates:
            if x[0] not in [m[0] for m in filtered_movies]:
                movie = df2.iloc[x[0]]
                movie_genres = set()
                if isinstance(movie.get('genres'), str):
                    try:
                        from ast import literal_eval
                        genres_list = literal_eval(movie.get('genres', '[]'))
                        movie_genres = set([g.get('name', '').lower() if isinstance(g, dict) else str(g).lower() for g in genres_list])
                    except:
                        pass
                elif isinstance(movie.get('genres'), list):
                    movie_genres = set([g.lower() if isinstance(g, str) else str(g).lower() for g in movie.get('genres', [])])
                
                exclude_genres = {'family', 'children', 'animation', 'horror', 'fantasy'}
                movie_has_excluded = len(movie_genres & exclude_genres) > 0
                
                # Skip excluded genres for action/sci-fi sources
                if source_genres and movie_genres:
                    action_sci_fi_genres = {'action', 'adventure', 'sciencefiction', 'sci-fi', 'science fiction', 'thriller', 'crime'}
                    source_is_action_sci_fi = len(source_genres & action_sci_fi_genres) > 0
                    movie_is_action_sci_fi = len(movie_genres & action_sci_fi_genres) > 0
                    
                    # Skip excluded genres
                    if source_is_action_sci_fi and movie_has_excluded and not movie_is_action_sci_fi:
                        continue  # Skip this movie
                    
                    # Also check similarity score - must be > 0.09 for single genre matches
                    genre_overlap_count = len(source_genres & movie_genres)
                    if source_is_action_sci_fi and movie_is_action_sci_fi:
                        if genre_overlap_count >= 2:
                            if x[1] <= 0.08:  # score too low for 2+ genres
                                continue
                        else:
                            if x[1] <= 0.09:  # score too low for single genre (excludes Cave Bear at 0.081)
                                continue
                    elif source_is_action_sci_fi:
                        # Source is action but movie is not - skip if score too low
                        if x[1] <= 0.08:
                            continue
                
                remaining.append((x[0], x[1], 0, 0))
                if len(remaining) >= (10 - len(filtered_movies)):
                    break
        
        filtered_movies.extend(remaining)
    
    movie_indices = [i[0] for i in filtered_movies[:10]]
    return df2['title'].iloc[movie_indices]

features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)
    
def get_director(x):
    for i in x:
        if (i['job'] == 'Director'):
            return i['name']
    return np.nan

def get_list(x):
    if (isinstance(x,list)):
        names = [i['name'] for i in x]
        if len(names) > 3:
            return names[:3]
        return names
    return []

df2['director'] = df2['crew'].apply(get_director)
features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)
    
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
        
features = ['cast', 'keywords', 'director', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(clean_data)
    
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df2['soup'] = df2.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])

if __name__ == "__main__":
    print(get_recommendations('The Conjuring')).tolist()