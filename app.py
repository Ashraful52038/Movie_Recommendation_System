import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Download from Google Drive (handles large files)
def download_file_from_google_drive(file_id, destination):
    if os.path.exists(destination):
        return

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)

    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# Add your Google Drive file IDs
download_file_from_google_drive("1iZgQtPZrNLXRoiGHMgoU2qlgTU4grih3", "movie_dict.pkl")
download_file_from_google_drive("1MnDzYKeaHJw-mdyon-b_mdqZsew9gmaV", "similarity.pkl")

# Load files
with open('movie_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)
movies = pd.DataFrame(movies_dict)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=267fdd6ab0dfe7bee4813dd75e6f979b')
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
selected_movie_name = st.selectbox('Choose your movie?', movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i])
