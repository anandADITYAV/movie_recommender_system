import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Create a session with retry logic
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def fetch_poster(movie_id):

    try:
        response = session.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e8193a8036e93a75fdf56f00624edf76',
            timeout=5  # Set timeout to 5 seconds
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id  # Use the 'id' column from your movies DataFrame
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Load the movie data and similarity matrix
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit App Interface
st.title("Movie Recommender System")

option = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(option)

    # Display recommendations in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    # st.markdown(reduced_size_css, unsafe_allow_html=True)

    with col1:
        st.markdown(f"<div class='subheader'>{names[0]}</div>", unsafe_allow_html=True)
        st.image(posters[0])

    with col2:
        st.markdown(f"<div class='subheader'>{names[1]}</div>", unsafe_allow_html=True)
        st.image(posters[1])

    with col3:
        st.markdown(f"<div class='subheader'>{names[2]}</div>", unsafe_allow_html=True)
        st.image(posters[2])

    with col4:
        st.markdown(f"<div class='subheader'>{names[3]}</div>", unsafe_allow_html=True)
        st.image(posters[3])

    with col5:
        st.markdown(f"<div class='subheader'>{names[4]}</div>", unsafe_allow_html=True)
        st.image(posters[4])