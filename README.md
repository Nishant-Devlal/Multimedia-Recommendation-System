# Multimedia Recommendation System

This is a Multimedia Recommendation System project that uses Content-based filtering to recommend users different types of media.
Right now it recommends songs, movies and books but since the code structure is modular we can just make another module like games and add it.
All the datasets used are given in Datasets folder in zip files, extract them and run the backend codes.
Once you run all the backend codes, you will get similarity and dataframe files.
Then run the frontend codes on the same folder.

To run front end codes you will need different API keys:
1. Spotify API key from spotify developer option
2. TMDB API key from TMDB website
3. Books API from Google Cloud Console
Use all these API keys then the project will run.

Note: To use Spotify api i.e spotipy, you will need premium subscription of Spotify.

# Architecture Diagram
<img width="381" height="431" alt="image" src="https://github.com/user-attachments/assets/a88161c4-72b4-454b-9e86-f8bedf880eee" />

# Evaluation Matrices
Recall@10  
r@10=|Relevant Items ∩ Top 10 recommendations| / |Relevant Items|  
For songs r@10=0.6  
For movies r@10=0.8  
For books r@10=0.5  

# Screenshots
1. Home Page:
    <img width="1566" height="725" alt="image" src="https://github.com/user-attachments/assets/b780e2d3-8f25-49d7-9d9c-444cca4a7c9f" />

2. Song Recommender:
   <img width="1574" height="733" alt="image" src="https://github.com/user-attachments/assets/9a4b20ff-71b6-4a7d-836e-42dd2b20e28a" />

3. Movie Recommender:
   <img width="1571" height="730" alt="image" src="https://github.com/user-attachments/assets/556dc67c-1beb-4c42-a030-ef923e9f7d01" />

4. Book Recommender:
   <img width="1566" height="722" alt="image" src="https://github.com/user-attachments/assets/fb0a3f47-a6f7-4327-8bd3-a2d385eb1e34" />

Try yourself at https://multimedia-recommendation-system-by-nishant-devlal.streamlit.app/
