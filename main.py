import streamlit as st
from songs import song_recommender
from movies import movie_recommender
from books import book_recommender
from home import home_page

st.set_page_config(page_title="Multimedia Recommendation System", layout="wide")

st.title("Multimedia Recommendation System")

choice = st.sidebar.radio("Select Recommendation Type", ["🏠 Home", "🎵 Songs", "🎬 Movies", "📚 Books"])

if choice == "🏠 Home":
    home_page()

elif choice == "🎵 Songs":
    song_recommender()

elif choice == "🎬 Movies":
    movie_recommender()

elif choice == "📚 Books":
    book_recommender()