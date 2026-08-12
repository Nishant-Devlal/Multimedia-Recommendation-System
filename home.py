import streamlit as st

def home_page():
    theme = st.radio("Choose Theme", ["Dark 🌙", "Light ☀️"], horizontal=True)
    is_dark = theme == "Dark 🌙"
    bg_color = "#000000" if is_dark else "#ffffff"
    text_color = "white" if is_dark else "black"

    st.markdown(f"""
            <style>
            .stApp {{
                background-color: {bg_color};
                color: {text_color};
            }}
            div[data-testid="stRadio"] * {{
                color: {text_color} !important;
            }}
            </style>
        """, unsafe_allow_html=True)

    st.markdown(
        f"<h1 style='color:{"#953BCC"}; text-align: center;'>Welcome</h1>",
        unsafe_allow_html=True)

    st.markdown(
        f"<h4 style='color:{"#953BCC"}; text-align: center;'>Discover your next favorite song, movie, or book</h4>",
        unsafe_allow_html=True)

    st.markdown("""
    <hr>
    <p style='text-align:center; color:gray;'>
    Built using Streamlit
    </p>
    """, unsafe_allow_html=True)
