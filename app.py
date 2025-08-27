import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Download from Hugging Face Datasets
def download_from_hf(url, destination):
    if os.path.exists(destination):
        return  # Skip if already downloaded

    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise error if download failed

    with open(destination, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)

# Your Hugging Face dataset repo (replace with your actual username/repo if different)
BASE_URL = "https://huggingface.co/datasets/Ashraful52038/movie-recommendation-files/resolve/main/"

download_from_hf(BASE_URL + "movie_dict.pkl", "movie_dict.pkl")
download_from_hf(BASE_URL + "similarity.pkl", "similarity.pkl")

# Load files safely
with open("movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)
movies = pd.DataFrame(movies_dict)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=267fdd6ab0dfe7bee4813dd75e6f979b"
    )
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies, recommended_movies_poster

# Streamlit UI
st.title("Movie Recommendation System")
selected_movie_name = st.selectbox("Choose your movie?", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i])
