import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=fea170440f16f94204650235a68988d0'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

theme = st.radio("Choose Theme", ["🌙", "☀️"], horizontal=True)
is_dark = theme == "🌙"

if is_dark:
    bg_color = "#000000"
    text_color = "#FFFFFF"
    card_bg = "#141414"
    button_color = "#E50914"
    button_hover = "#B20710"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    card_bg = "#f0f0f0"
    button_color = "#E50914"
    button_hover = "#B20710"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    div.stButton > button:first-child {{
        background-color: {button_color};
        color: white;
        border: None;
        padding: 0.5em 1em;
        border-radius: 25px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }}
    div.stButton > button:first-child:hover {{
        background-color: {button_hover};
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 style='color: {button_color}; text-align: center;'>Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='color: {text_color};'>Type or select a movie from the dropdown</h4>", unsafe_allow_html=True)
selected_movie = st.selectbox("", movies['title'].values)

if st.button("Recommend"):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(
                f"""
                <div style='
                    background-color: {card_bg};
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                '>
                    <img src="{posters[i]}" width="150" style='border-radius: 8px'><br>
                    <strong style='color: {text_color}'>{names[i]}</strong><br>
                    <a href="https://www.themoviedb.org/movie/{movies[movies['title']==names[i]].movie_id.values[0]}" target="_blank" style='color: {button_color}; font-weight: bold;'>▶ View on TMDB</a>
                </div>
                """,
                unsafe_allow_html=True
            )