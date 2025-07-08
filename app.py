from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

# Step 1: Load models
SIMILARITY_PATH = "similarity.pkl"
MOVIES_PATH = "movies.pkl"

# Ensure the required files exist
if not os.path.exists(SIMILARITY_PATH):
    raise FileNotFoundError("similarity.pkl not found. It should be downloaded during build.")

if not os.path.exists(MOVIES_PATH):
    raise FileNotFoundError("movies.pkl not found. Please make sure it's in your repo.")

movies = pickle.load(open(MOVIES_PATH, 'rb'))  # DataFrame
similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))
movie_titles = movies['title'].values

# Step 2: Fetch poster from OMDB
def get_movie_poster(title):
    formatted_title = title.replace(" ", "+")
    url = f"https://www.omdbapi.com/?t={formatted_title}&apikey=a2d175f4"
    response = requests.get(url)
    data = response.json()
    return data.get("Poster")

# Step 3: Recommend movies using similarity matrix
def recommend(movie):
    if movie not in movies['title'].values:
        return []

    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommendations = []
    for i in movie_indices:
        title = movies.iloc[i[0]].title
        poster = get_movie_poster(title)
        recommendations.append((title, poster))
    return recommendations

# Step 4: Flask routes
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', movie_list=movie_titles, recommended_movies=[], selected_movie="")

@app.route('/recommend', methods=['POST'])
def recommend_route():
    selected_movie = request.form['movie']
    recommendations = recommend(selected_movie)
    return render_template('index.html', movie_list=movie_titles, recommended_movies=recommendations, selected_movie=selected_movie)

# Step 5: Run the app
if __name__ == '__main__':
    app.run(debug=True)