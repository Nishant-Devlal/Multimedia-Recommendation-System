import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def song_recommender():
    CLIENT_ID = "46a307ffb8d44f41bb5aafdc81540b89"
    CLIENT_SECRET = "9d7dceceaf58483e919985e7567dfbcb"

    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def fetch_trending_songs(sp, limit=20):
        results = sp.new_releases(country="IN", limit=limit)
        songs = []
        for album in results['albums']['items']:
            songs.append({
                "title": album['name'],
                "artist": album['artists'][0]['name'],
                "cover": album['images'][0]['url'],
                "link": album['external_urls']['spotify']
            })
        return songs

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

    def recommend(song, music, similarity, song_col="song", artist_col="artist"):
        index = music[music[song_col] == song].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        names, posters, links = [], [], []
        for x in distances[1:6]:
            artist = music.iloc[x[0]][artist_col]
            song_name = music.iloc[x[0]][song_col]
            album_cover_url, track_url = get_song_album_cover_and_url(song_name, artist)
            names.append(song_name)
            posters.append(album_cover_url)
            links.append(track_url)
        return names, posters, links

    def recommend_by_mood(mood):
        mood_songs = english_music[english_music['mood'].str.lower() == mood.lower()]
        recommended_music_names = []
        recommended_music_posters = []
        recommended_music_links = []
        for i, row in mood_songs.head(30).iterrows():
            album_cover_url, track_url = get_song_album_cover_and_url(row['song'], row['artist'])
            recommended_music_names.append(row['song'])
            recommended_music_posters.append(album_cover_url)
            recommended_music_links.append(track_url)
        return recommended_music_names, recommended_music_posters, recommended_music_links

    hindi_music = pickle.load(open("Hindi/hindi_df", "rb"))
    hindi_similarity = pickle.load(open("Hindi/hindi_similarity", "rb"))
    english_music = pickle.load(open("English/english_df", "rb"))
    english_similarity = pickle.load(open("English/english_similarity", "rb"))

    theme = st.radio("Choose Theme", ["Dark 🌙", "Light ☀️"], horizontal=True)
    is_dark = theme == "Dark 🌙"
    bg_color = "#000000" if is_dark else "#ffffff"
    text_color = "white" if is_dark else "black"
    card_bg = "#5E575C" if is_dark else "#f0f0f0"
    button_color = "#409128"
    button_hover = "#77FF63"

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
        div[data-testid="stRadio"] * {{
            color: {text_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Trending Songs", "Hindi Songs", "English Songs"])

    with tab1:
        st.markdown("""
            <style>
            .stTabs [data-baseweb="tab"] {
                background-color: #f0f0f0;
                color: black;
                border-radius: 10px;
                padding: 6px 12px;
                margin: 2px;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #409128;
                color: white;
                border-radius: 10px;
            }
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #77FF63;
                color: black;
                border-radius: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(f"<h2 style='color:{button_color}; text-align: center;'>Song Recommender</h2>",unsafe_allow_html=True)
        st.subheader("🔥 Trending Songs")
        trending = fetch_trending_songs(sp, limit=20)
        for row in range(4):
            cols = st.columns(5)
            for i in range(5):
                idx = row * 5 + i
                if idx < len(trending):
                    with cols[i]:
                        st.markdown(f"""
                                <div style='
                                    background-color:{card_bg};
                                    padding:10px;
                                    border-radius:10px;
                                    text-align:center;'>
                                    <img src="{trending[idx]['cover']}" width="150" style='border-radius:8px'><br>
                                    <strong style='color:{text_color}'>{trending[idx]['title']}</strong><br>
                                    <em style='color:{button_color}'>{trending[idx]['artist']}</em><br>
                                    <a href="{trending[idx]['link']}" target="_blank"
                                       style='color:{button_hover}; font-weight:bold;'>🎧 Listen on Spotify</a>
                                </div>
                            """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"<h2 style='color:{button_color}; text-align: center;'>Hindi Song Recommender</h2>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color: {text_color};'>Type or select a Hindi song from the dropdown:</h4>", unsafe_allow_html=True)
        selected_song = st.selectbox("", hindi_music["music_name"].values)
        if st.button("Recommend Hindi"):
            with st.spinner("Fetching Hindi recommendations..."):
                names, posters, links = recommend(selected_song, hindi_music, hindi_similarity, song_col="music_name", artist_col="singer")
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    st.markdown(f"""
                        <div style='background-color:{card_bg};padding:10px;border-radius:10px;text-align:center;'>
                            <img src="{posters[i]}" width="150" style='border-radius:8px'><br>
                            <strong style='color:{text_color}'>{names[i]}</strong><br>
                            <a href="{links[i]}" target="_blank" style='color:{button_hover};'>🎧 Listen on Spotify</a>
                        </div>
                        """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"<h2 style='color:{button_color}; text-align: center;'>English Song Recommender</h2>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color: {text_color};'>Type or select an English song from the dropdown:</h4>", unsafe_allow_html=True)
        selected_song = st.selectbox("", english_music["song"].values)
        if st.button("Recommend English"):
            with st.spinner("Fetching English recommendations..."):
                names, posters, links = recommend(selected_song, english_music, english_similarity, song_col="song", artist_col="artist")
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    st.markdown(f"""
                        <div style='background-color:{card_bg};padding:10px;border-radius:10px;text-align:center;'>
                            <img src="{posters[i]}" width="150" style='border-radius:8px'><br>
                            <strong style='color:{text_color}'>{names[i]}</strong><br>
                            <a href="{links[i]}" target="_blank" style='color:{button_hover};'>🎧 Listen on Spotify</a>
                        </div>
                        """, unsafe_allow_html=True)

        mood_choice = st.radio("Choose Mood", ["Happy", "Sad", "Calm"], horizontal=True)

        if st.button("Recommend by Mood"):
            with st.spinner(f"Fetching {mood_choice} songs..."):
                recommended_music_names, recommended_music_posters, recommended_music_links = recommend_by_mood(mood_choice)
            cols = st.columns(5)
            for i in range(len(recommended_music_names)):
                with cols[i % 5]:
                    st.markdown(f"""
                        <div style='
                            background-color: {card_bg};
                            padding: 10px;
                            border-radius: 10px;
                            text-align: center; '>
                            <img src="{recommended_music_posters[i]}" width="150" style='border-radius: 8px'><br>
                            <strong style='color: {text_color}'>{recommended_music_names[i]}</strong><br>
                            <a href="{recommended_music_links[i]}" target="_blank" style='color: {button_hover};'>🎧 Listen on Spotify</a>
                        </div>
                        """, unsafe_allow_html=True)
