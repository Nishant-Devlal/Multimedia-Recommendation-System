import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "enter_your_client_id"
CLIENT_SECRET = "enter_your_client_secret"

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_and_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        track_url = track["external_urls"]["spotify"]
        return album_cover_url, track_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png", "#"

def recommend(music_name):
    index = music[music['music_name'] == music_name].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_links = []

    for x in distances[1:6]:
        song = music.iloc[x[0]].music_name
        singer = music.iloc[x[0]].singer
        album_cover_url, track_url = get_song_album_cover_and_url(song, singer)
        recommended_music_names.append(song)
        recommended_music_posters.append(album_cover_url)
        recommended_music_links.append(track_url)
    return recommended_music_names, recommended_music_posters, recommended_music_links

music = pickle.load(open("hindi_df", "rb"))
similarity = pickle.load(open("hindi_similarity", "rb"))
music_list = music["music_name"].values

theme = st.radio("Choose Theme", ["🌙", "☀️"], horizontal=True)
is_dark = theme == "🌙"

bg_color = "#000000" if is_dark else "#ffffff"
text_color = "white" if is_dark else "black"
card_bg = "#5E575C" if is_dark else "#f0f0f0"
button_color = "#409128"
button_hover = "#77FF63"

if is_dark:
    st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
            color: white;
        }
        label, .stRadio > div {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: black;
        }
        label, .stRadio > div {
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

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

st.markdown(f"<h1 style='color: {button_color}; text-align: center;'>Hindi Song Recommender</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='color: {text_color};'>Type or select a song from the dropdown</h4>", unsafe_allow_html=True)
selected_song = st.selectbox("", music_list)

if st.button("Recommend"):
    with st.spinner("Fetching recommendations..."):
        recommended_music_names, recommended_music_posters, recommended_music_links = recommend(selected_song)
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
                    <img src="{recommended_music_posters[i]}" width="150" style='border-radius: 8px'><br>
                    <strong style='color: {text_color}'>{recommended_music_names[i]}</strong><br>
                    <a href="{recommended_music_links[i]}" target="_blank" style='color: {button_hover};'>🎧 Listen on Spotify</a>
                </div>
                """,
                unsafe_allow_html=True
            )

