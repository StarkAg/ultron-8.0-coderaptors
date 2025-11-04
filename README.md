# Ultron 8.0 - CodeRaptors: Movie & TV Show Recommendation System

An intelligent movie and TV show recommendation system built with Flask, machine learning, and sentiment analysis.

## 🎬 Project Overview

This project is a comprehensive entertainment recommendation platform that provides personalized movie and TV show suggestions based on user preferences. The system uses machine learning algorithms, sentiment analysis, and poster/image fetching to deliver an enhanced user experience.

## ✨ Key Features

- **Movie Recommendations**: Get personalized movie suggestions based on your preferences
- **TV Show Recommendations**: Discover new TV shows tailored to your taste
- **Genre Mixing**: Intelligent genre combination for diverse recommendations
- **Poster Integration**: Automatic poster fetching for recommended content
- **Sentiment Analysis**: Analyze sentiment from reviews and descriptions
- **Interactive Web Interface**: Clean, user-friendly Flask web application
- **Watch Party Features**: Collaborative watching features

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn, pandas, numpy
- **Data Processing**: Jupyter Notebooks
- **Image API**: SerpAPI for poster fetching
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: CSV datasets

## 📋 Prerequisites

- Python 3.8+
- pip
- Flask
- Required Python packages (see installation)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/StarkAg/ultron-hackathon.git
cd "Ultron 8.0- CodeRaptors"
```

### 2. Install Dependencies

```bash
pip install flask pandas numpy scikit-learn serpapi
```

### 3. Set Up API Key

1. Get a SerpAPI key from [serpapi.com](https://serpapi.com)
2. Create `api_key.py` file:
   ```python
   API_KEY = "your-serpapi-key-here"
   ```

### 4. Prepare Datasets

Ensure the following datasets are in the `datasets/` folder:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`
- `TMDB_tv_dataset_v3.csv`
- `train.csv`
- `test.csv`

## 🚀 Usage

### Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using Jupyter Notebooks

1. **Movie Recommender System:**
   ```bash
   jupyter notebook Movie_Recommender_System.ipynb
   ```

2. **TV Show Recommender System:**
   ```bash
   jupyter notebook TVShow_Recommender_System_Optimized.ipynb
   ```

3. **Sentiment Analysis:**
   ```bash
   jupyter notebook SentimentV2.ipynb
   ```

## 📁 Project Structure

```
Ultron 8.0- CodeRaptors/
├── app.py                          # Main Flask application
├── Movie_Recommendations.py        # Movie recommendation logic
├── Shows_Recommendations.py        # TV show recommendation logic
├── GenreMixing.py                 # Genre combination algorithms
├── Posters.py                     # Poster fetching utilities
├── WatchParty.py                  # Watch party features
├── api_key.py                     # API key configuration (create this)
├── datasets/                      # CSV datasets
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   ├── TMDB_tv_dataset_v3.csv
│   ├── train.csv
│   └── test.csv
├── templates/                     # HTML templates
│   └── frontend/
│       ├── index.html
│       ├── Movies.html
│       ├── shows.html
│       ├── TV.html
│       └── ...
├── static/                        # Static assets
│   └── images/
├── Movie_Recommender_System.ipynb # Movie ML notebook
├── TVShow_Recommender_System_Optimized.ipynb # TV ML notebook
└── SentimentV2.ipynb              # Sentiment analysis notebook
```

## 🎯 Features Breakdown

### Movie Recommendations
- Content-based filtering
- Genre-based suggestions
- Similarity scoring
- Poster integration

### TV Show Recommendations
- Optimized recommendation algorithms
- Genre matching
- Rating-based filtering
- Show poster display

### Genre Mixing
- Intelligent genre combination
- Multi-genre recommendations
- Diverse content suggestions

### Sentiment Analysis
- Review sentiment classification
- Description analysis
- User preference learning

## 🔐 Configuration

### API Keys Required

1. **SerpAPI Key**: For fetching movie/TV show posters
   - Sign up at: https://serpapi.com
   - Add to `api_key.py`

## 📊 Datasets

The project uses TMDB (The Movie Database) datasets:
- 5000+ movies with metadata
- 5000+ movie credits
- TV show dataset (v3)
- Training and test datasets

## 🧪 Testing

```bash
python test.py
```

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

1. Use a WSGI server (Gunicorn, uWSGI)
2. Set up environment variables
3. Configure API keys securely
4. Deploy to platforms like:
   - Heroku
   - Render
   - Railway
   - AWS/GCP

## 📝 Usage Examples

### Get Movie Recommendations

1. Navigate to the home page
2. Select "Movies"
3. Enter a movie name
4. Get personalized recommendations with posters

### Get TV Show Recommendations

1. Select "TV Shows"
2. Enter a show name
3. Receive similar show suggestions

## 🎯 Hackathon Details

- **Event**: Ultron 8.0 Hackathon
- **Team**: CodeRaptors
- **Category**: AI/ML, Web Development
- **Status**: Completed

## 🤝 Contributing

This is a hackathon project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of a hackathon submission. All rights reserved.

## 👥 Team

- **CodeRaptors Team**

## 🙏 Acknowledgments

- TMDB for dataset access
- SerpAPI for image search
- Flask community
- Machine learning libraries contributors

---

**Built with ❤️ by CodeRaptors for Ultron 8.0 Hackathon**
