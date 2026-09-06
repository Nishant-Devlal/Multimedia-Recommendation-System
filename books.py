import streamlit as st
import pickle
import numpy as np
import requests

def book_recommender():
    popular_df = pickle.load(open("popular.pkl", "rb"))
    pt = pickle.load(open("pt.pkl", "rb"))
    similarity_scores = pickle.load(open("Similarity_scores.pkl", "rb"))
    books = pickle.load(open("books.pkl", "rb"))

    @st.cache_data(ttl=3600)

    def recommend(book_name):
        matches = np.where(pt.index == book_name)[0]
        if len(matches) == 0:
            return []
        index = matches[0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1],reverse=True)[1:6]
        data = []
        for i in similar_items:
            title = pt.index[i[0]]
            temp_df = books[books['Book-Title']==title]
            if not temp_df.empty:
                book_title = temp_df['Book-Title'].values[0]
                author = temp_df['Book-Author'].values[0]
                poster = temp_df['Image-URL-M'].values[0]
            else:
                book_title = title
                author = "Unknown"
                poster = "https://via.placeholder.com/150x220?text=No+Image"
            data.append([poster, book_title, author])
        return data

    theme = st.radio("Choose Theme", ["Dark 🌙", "Light ☀️"], horizontal=True)
    is_dark = theme == "Dark 🌙"

    bg_color = "#000000" if is_dark else "#ffffff"
    text_color = "white" if is_dark else "black"
    card_bg = "#141414" if is_dark else "#f0f0f0"
    button_color = "#001EFF"
    button_hover = "#039AFF"

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

    tab1, tab2, tab3 = st.tabs(["Popular Books", "Recommend Books"])

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
            background-color: #001EFF;
            color: white;
            border-radius: 10px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #001EFF;
            color: white;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    with tab1:
        st.markdown(f"<h2 style='color:{button_color}; text-align:center;'>Most Popular Books</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <style>
            .book-card {{
                background-color:{card_bg};
                padding:15px;
                border-radius:12px;
                text-align:center;
                min-height:320px;
                display:flex;
                flex-direction:column;
                justify-content:space-between;
                box-shadow:0 4px 8px rgba(0,0,0,0.2);
                transition:transform 0.3s ease, box-shadow 0.3s ease;
            }}
            .book-card:hover {{
                transform: scale(1.05);
                box-shadow:0 8px 16px rgba(0,0,0,0.3);
            }}
            .book-title {{
                color:{text_color};
                font-size:16px;
                font-weight:bold;
                margin-top:8px;
            }}
            .book-author {{
                color:{button_color};
                font-size:14px;
                font-weight:bold;
            }}
            .book-rating {{
                color:{button_hover};
                font-size:13px;
            }}
            </style>
        """, unsafe_allow_html=True)

        for i in range(0, len(popular_df), 5):
            cols = st.columns(5)
            for j, col in enumerate(cols):
                if i + j < len(popular_df):
                    row = popular_df.iloc[i + j]
                    book_link = f"https://www.goodreads.com/search?q={row['Book-Title'].replace(' ', '+')}"
                    with col:
                        st.markdown(f"""
                            <a href="{book_link}" target="_blank" style="text-decoration:none;">
                            <div class="book-card">
                            <img src="{row['Image-URL-M']}" height="180" style='border-radius:8px; margin-bottom:10px;'>
                            <div class="book-title">{row['Book-Title']}</div>
                            <div class="book-author">{row['Book-Author']}</div>
                            <div class="book-rating">⭐ {round(row['avg_ratings'], 1)} ({row['num_ratings']} ratings)</div>
                            </div>
                            </a>
                            """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"<h2 style='color:{button_color}; text-align:center;'>Find Similar Books</h2>", unsafe_allow_html=True)
        selected_book = st.selectbox("Select a book:", pt.index)

        if st.button("Recommend"):
            with st.spinner("Fetching recommendations..."):
                data = recommend(selected_book)

            cols = st.columns(5)
            for i, col in enumerate(cols):
                if i < len(data):
                    poster, title, author = data[i]
                    with col:
                        st.markdown(
                            f"""
                            <div style='
                                background-color:{card_bg};
                                padding:15px;
                                border-radius:12px;
                                text-align:center;
                                box-shadow:0 4px 8px rgba(0,0,0,0.2);
                                transition:transform 0.3s ease;'>
                                <a href="https://www.goodreads.com/search?q={title}" target="_blank">
                                <img src="{poster}" height="180" style='border-radius:8px'>
                                </a><br>
                                <strong style='color:{text_color}; font-size:16px;'>{title}</strong><br>
                                <em style='color:#001EFF; font-weight:bold;'>{author}</em><br>
                                <span style='color:{button_color};'>⭐ {round(row['avg_ratings'], 1)} ({row['num_ratings']} ratings)</span>
                            </div>
                            """, unsafe_allow_html=True)
