from flask import Flask, request, jsonify,render_template
from pydantic import BaseModel
import pandas as pd
import joblib
import requests
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

# Load necessary data
movies_new = pd.read_csv('D:\\projects\\ML\\content_recomm\\movies_data.csv')  # Assuming you saved your preprocessed data
similarity_matrix = joblib.load('D:\\projects\\ML\\content_recomm\\similarity_matrix.pkl')  # Load cosine similarity matrix
model = joblib.load('D:\\projects\\ML\\content_recomm\\vectors.pkl')  # Load your trained model
cv = CountVectorizer(max_features=5000, stop_words='english')
ps = PorterStemmer()


TMDB_API_KEY = '6656d36c53e195637fd4d24c2d7a1a74'
# Initialize Flask app
app = Flask(__name__)

# Define request body model
# class MovieInput(BaseModel):
#     title: str
@app.route("/")
def index():
    return render_template("index.html")


# Define recommendation endpoint
@app.route("/recommend/<title>", methods=["GET","POST"])
def recommend_movies(title):
    # Parse request body
    # movie_input = request.json
    # title = movie_input['title']
    
    # Make prediction based on user input
    try:
        movie_index = movies_new[movies_new['title'] == title].index[0]
        distances = similarity_matrix[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = [movies_new.iloc[i[0]].title for i in movies_list]

        recommended_movies_with_images = []
        for movie in recommended_movies:
            image_url = get_movie_image(movie)
            recommended_movies_with_images.append({'title': movie, 'image_url': image_url})

        return jsonify(recommended_movies_with_images)
    except IndexError:
        return jsonify({"error": "Movie not found in dataset"}), 404
def get_movie_image(title):
    url =  f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None
if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=8000)
    app.run(debug=True)
