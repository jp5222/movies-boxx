from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

# Google Drive direct download link for similarity.pkl
SIMILARITY_URL = "https://drive.google.com/uc?export=download&id=1eaRn28XCyrjwzAhWfB_C8yNHtRSNK3Mi"
SIMILARITY_PATH = "similarity.pkl"

# Step 1: Download similarity.pkl from Google Drive if missing
def download_similarity():
    if not os.path.exists(SIMILARITY_PATH):
        print("Downloading similarity.pkl from Google Drive...")
        response = requests.get(SIMILARITY_URL)
        with open(SIMILARITY_PATH, "wb") as f:
            f.write(response.content)
        print("Downloaded similarity.pkl")

# Step 2: Load models
download_similarity()
movies = pickle.load(open('movies.pkl', 'rb'))  # DataFrame
similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))

movie_titles = movies['title'].values

# Step 3: Fetch poster from OMDB
def get_movie_poster(title):
    formatted_title = title.replace(" ", "+")
    url = f"https://www.omdbapi.com/?t={formatted_title}&apikey=a2d175f4"
    response = requests.get(url)
    data = response.json()
    return data.get("Poster")

# Step 4: Recommend movies using similarity matrix
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

# Step 5: Flask routes
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', movie_list=movie_titles, recommended_movies=[], selected_movie="")

@app.route('/recommend', methods=['POST'])
def recommend_route():
    selected_movie = request.form['movie']
    recommendations = recommend(selected_movie)
    return render_template('index.html', movie_list=movie_titles, recommended_movies=recommendations, selected_movie=selected_movie)

if __name__ == '__main__':
    app.run(debug=True)


