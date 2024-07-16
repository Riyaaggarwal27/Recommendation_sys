import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def recommend_movies(title):
    response = requests.get(f"http://127.0.0.1:5000/recommend/{title}")
    return response.json()

st.set_page_config(page_title="Recommendation",page_icon=":star:",layout="wide")

st.write('<h1>Movie Recommendation System</h1>',unsafe_allow_html=True)

movie_title = st.text_input('Enter a movie title:', 'Batman')

if st.button('Recommend'):
    recommendations = recommend_movies(movie_title)
    if isinstance(recommendations,dict)and 'error' in recommendations:
        st.write(recommendations['error'])
    elif isinstance(recommendations,list):
        st.write('Recommendations for', movie_title, ':')
        cols=st.columns(5)
        for index,movie in enumerate(recommendations):
            col=cols[index%5]
            with col:
                st.write(movie['title'])
                if movie['image_url']:
                    response = requests.get(movie['image_url'])
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_column_width=True)
                else:
                    st.write("Image not found")
    else:
        st.write("unexpected response format")