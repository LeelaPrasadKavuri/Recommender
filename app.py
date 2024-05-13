import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w200/" + poster_path  # Reduced size to w200
    return full_path

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    details = {
        'title': data['title'],
        'overview': data['overview'],
        'rating': data['vote_average'],
        'release_date': data['release_date'],
        'poster': "https://image.tmdb.org/t/p/w200/" + data['poster_path']  # Reduced size to w200
    }
    return details

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(fetch_movie_details(movie_id))
    return recommended_movies

st.set_page_config(page_title='Movie Recommender System', layout='wide')

# Load the data
with open('movies.pkl', 'rb') as file:
    movies = pd.read_pickle(file)
with open('similarity.pkl', 'rb') as file:
    similarity = pd.read_pickle(file)

# Additional CSS to reduce space and add padding/margin
custom_css = '''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-18e3th9 {
    padding-top: 1rem;
}
.stButton button {
    margin-top: 1rem;
    background-color: #4CAF50; 
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
}
.stButton button:hover {
    background-color: #45a049;
}
.movie-container {
    display: flex;
    align-items: center;
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.movie-poster {
    max-width: 150px;  # Set the max-width to a smaller size
    border-radius: 10px;
    margin-right: 20px;
}
.movie-details {
    flex: 1;
}
.movie-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 10px;
}
.movie-rating {
    color: #f39c12;
    font-size: 1.2rem;
    margin-bottom: 5px;
}
.movie-release-date, .movie-overview {
    color: #2c3e50;
    font-size: 1rem;
}
.movie-overview {
    margin-top: 10px;
}
</style>
'''

st.markdown(custom_css, unsafe_allow_html=True)

st.sidebar.markdown("## Find similar movies from a dataset of 5,000 movies!")
selected_movie = st.sidebar.selectbox("Type or select a movie you like:", movies['title'].values)

st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🎬 Movie Recommender System 🎬</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; font-size: 1.5rem;'> Prasad Kavuri</h4>", unsafe_allow_html=True)

if st.sidebar.button('Show Recommendation'):
    st.markdown("<h2 style='text-align: center;'>Recommended Movies based on your interests are:</h2>", unsafe_allow_html=True)
    recommended_movies = recommend(selected_movie)
    for movie in recommended_movies:
        st.markdown(f"""
        <div class="movie-container">
            <img src="{movie['poster']}" class="movie-poster">
            <div class="movie-details">
                <p class="movie-title">{movie['title']}</p>
                <p class="movie-rating">⭐ Rating: {movie['rating']}</p>
                <p class="movie-release-date">📅 Release Date: {movie['release_date']}</p>
                <p class="movie-overview">{movie['overview']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)















