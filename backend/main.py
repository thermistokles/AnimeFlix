from flask import Flask, request, jsonify
import requests
from models.user import User
import json
from flask_cors import CORS
from util.Recommendation import recommend_animes_by_genres_only
from util.Recommendation import recommend_animes_for_user
from util.test1 import recommend_animes_based_on_search, search_animes, filter_animes_by_age, preprocess_title_and_genre, df_anime
from util.Recommendation import recommend_animes_for_user, find_k_similar_users, recommend_animes_for_user,find_k_similar_users,loaded_user_similarity_matrix_sparse,recommend_animes_by_genres_only,is_18_above,recommend_animes_by_titles,get_anime_title,animes_copy,get_anime_id,extract_genres,get_genre_score
from util.Neural_Network import display
from util.content_based import recommend

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

loggedInUsers = [{'username': 'DesolatePsyche', 'password': 'DesolatePsyche', 'genres': ['Action', 'Comedy', 'Drama', 'Horror'], 'isOver18': '24', 'movieShow': 'Show'}]

topRecommendedAnime = []


@app.route('/')
def hello():
    return 'Hello, World!'

@app.post('/register')
def register():
    data = request.json

    for user in loggedInUsers:
        if data['username'] == user['username']:
            return "User already exists, try logging in"
    loggedInUsers.append(data)
    return "registered successfully"

    # if data not in loggedInUsers:
    #     loggedInUsers.append(data)
    #     return "registered successfully"
    # recommend_animes_by_genres_only(data["genres"], age=data["isOver18"], type=data["movieShow"])
    # else:
    #     return "User already exists, try logging in"
    
@app.post('/login')
def login():
    data = request.json
    
    for user in loggedInUsers:
        if data['username'] == user['username'] and data['password'] == user['password']:
            print("data['username']: ", data['username'])
            return "Logged In"
    return "user does not exist"

@app.post('/newUserData')
def newUserData():
    data = request.json
    print("data: ", data)

    recommendations = recommend_animes_by_genres_only(data["genres"], age=data["isOver18"], type=data["movieShow"])
    recommended_anime_df = animes_copy[animes_copy['title'].isin(recommendations)]
    response_data = recommended_anime_df[['title', 'img_url', 'link']].to_dict('records')

    return jsonify(response_data)

@app.post('/existingUserData')
def existingUserData():
    data = request.json
    recommendations = recommend_animes_for_user(data['username'])
    recommended_anime_df = animes_copy[animes_copy['title'].isin(recommendations)]
    response_data = recommended_anime_df[['title', 'img_url', 'link']].to_dict('records')
    return jsonify(response_data)

@app.post('/search')
def search():
    data = request.json
    search_query = data['searchText']
    N = 20
    user_age = 14
    restricted_genres = ['Hentai', 'Ecchi', 'Harem', 'Yuri', 'Yaoi']
    searched_animes = search_animes(df_anime, search_query, N)
    searched_animes = filter_animes_by_age(searched_animes, user_age, restricted_genres)
    response_data = searched_animes[['anime_id', 'title','img_url','link']].to_dict('records')
    
    return jsonify(response_data)

@app.post('/content')
def search_content():
    request_data = request.json
    search_query = request_data['clickedAnime']
    search_query = search_query.lower()
    searched_animes = recommend(search_query,5, 15)
    return jsonify(searched_animes)
    
@app.post('/topRatedRecommendations')
def topRatedRecommendations():
    user = request.json
    recommendations = display(user['username'])
    #append_data(user['username'], 0, 0)

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run()
    