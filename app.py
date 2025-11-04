from flask import Flask, render_template, request, redirect, url_for
from api_key import API_KEY
import Movie_Recommendations
import Shows_Recommendations
import serpapi

app = Flask(__name__)

def GET_MoviePosters(movie):
    movies = Movie_Recommendations.get_recommendations(movie).tolist()
    movie_dict = {}
    for i in movies:
        # Search specifically for movie poster to avoid book covers
        params = {
        "q": f"{i} movie poster",
        "engine": "google_images",
        "hl": 'en',
        "ijn": "0",
        "api_key": API_KEY
        }
        search = serpapi.search(params)
        if 'images_results' in search and search['images_results']:
            # Try to find a poster image (look through first few results)
            image_link = None
            for result in search['images_results'][:5]:
                # Check if it's likely a poster (has "poster" in title or looks like a poster)
                title = result.get('title', '').lower()
                if 'poster' in title or 'movie' in title or 'film' in title:
                    image_link = result.get('original') or result.get('link')
                    break
            # If no poster found, use first result
            if not image_link:
                image_link = search['images_results'][0].get('original') or search['images_results'][0].get('link')
            movie_dict[i] = image_link
        else:
            movie_dict[i] = "No Image Found"
    
    return movie_dict

def GET_ShowsPosters(show):
    shows = Shows_Recommendations.get_recommendations(show).tolist()
    show_dict = {}
    for i in shows:
        params = {
        "q": i,
        "engine": "google_images",
        "hl": 'en',
        "ijn": "0",
        "api_key": API_KEY
        }
        search = serpapi.search(params)
        if 'images_results' in search and search['images_results']:
            image_link = search['images_results'][0]['original']
            show_dict[i] = image_link  # Store the movie name as key and image link as value
        else:
            show_dict[i] = "No Image Found"  # If no image is found, mark as "No Image Found"
    
    return show_dict

@app.route('/',methods=['GET'])
def index():
    return render_template('frontend/index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('frontend/loginpage.html')

@app.route('/choice', methods=['GET','POST'])
def choice():
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        if movie_name:
            try:
                posters = GET_MoviePosters(movie_name)
                # Pass posters directly to movies page instead of redirecting
                return render_template('frontend/Movies.html', posters=posters, movie_name=movie_name)
            except ValueError as e:
                # Movie not found - show user-friendly error
                error_msg = str(e)
                return render_template('frontend/choice.html', error=error_msg, movie_name=movie_name), 400
            except Exception as e:
                return render_template('frontend/choice.html', error=f"Error processing request: {str(e)}", movie_name=movie_name), 500
        else:
            return render_template('frontend/choice.html', error="Please enter a movie name"), 400
    return render_template('frontend/choice.html')


@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        if movie_name:
            try:
                posters = GET_MoviePosters(movie_name)
                return render_template('frontend/Movies.html', posters=posters, movie_name=movie_name)
            except ValueError as e:
                return render_template('frontend/Movies.html', error=str(e), movie_name=movie_name), 400
            except Exception as e:
                return render_template('frontend/Movies.html', error=f"Error processing request: {str(e)}", movie_name=movie_name), 500
        else:
            return render_template('frontend/Movies.html', error="Please enter a movie name"), 400
    # Handle GET requests with movie_name parameter (from direct URL access)
    movie_name = request.args.get('movie_name')
    if movie_name:
        try:
            posters = GET_MoviePosters(movie_name)
            return render_template('frontend/Movies.html', posters=posters, movie_name=movie_name)
        except Exception as e:
            return render_template('frontend/Movies.html', error=f"Error: {str(e)}", movie_name=movie_name), 400
    return render_template('frontend/Movies.html')

@app.route('/shows', methods=['GET', 'POST'])
def shows():
    if request.method == 'POST':
        show_name = request.form.get('show_name')
        if show_name:
            try:
                posters = GET_ShowsPosters(show_name)
                return render_template('frontend/shows.html', posters=posters)
            except Exception as e:
                return f"Error: {str(e)}", 500
        else:
            return "Show name is required", 400
    return render_template('frontend/shows.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)