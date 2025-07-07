from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))  # DataFrame
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_titles = movies['title'].values

def get_movie_poster(title):
    formatted_title = title.replace(" ", "+")
    url = f"https://www.omdbapi.com/?t={formatted_title}&apikey=a2d175f4"
    response = requests.get(url)
    data = response.json()
    return data.get("Poster")

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

