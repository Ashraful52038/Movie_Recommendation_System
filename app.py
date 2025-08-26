import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Function to download files if not present
def download_file(url, local_path):
    if not os.path.exists(local_path):
        r = requests.get(url)
        with open(local_path, 'wb') as f:
            f.write(r.content)

# Add your Google Drive direct download links here
download_file("https://drive.google.com/file/d/1iZgQtPZrNLXRoiGHMgoU2qlgTU4grih3/view?usp=drive_link", "movie_dict.pkl")
download_file("https://drive.google.com/file/d/1MnDzYKeaHJw-mdyon-b_mdqZsew9gmaV/view?usp=drive_link", "similarity.pkl")

# Load files
with open('movie_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)
movies = pd.DataFrame(movies_dict)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=267fdd6ab0dfe7bee4813dd75e6f979b'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommend_movies.append(movies.iloc[i[0]].title)
        # Fetch Poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies,recommended_movies_poster


# movies_dict=pickle.load(open('movie_dict.pkl','rb'))
# movies=pd.DataFrame(movies_dict)

# with gzip.open('similarity.pkl.gz', 'rb') as f:
#     similarity = pickle.load(f)

# Streamlit UI
st.title("Movie Recommendation System")

# Add a selectbox to the sidebar:
selected_movie_name= st.selectbox(
    'Choose your movie?',
movies['title'].values)

if st.button("Recommend"):
    names,posters =recommend(selected_movie_name)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i])