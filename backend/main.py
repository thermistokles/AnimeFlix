from flask import Flask, request, jsonify
import requests
from models.user import User
import json
from flask_cors import CORS
from util.Recommendation import recommend_animes_by_genres_only
from util.Recommendation import recommend_animes_for_user

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

    if data not in loggedInUsers:
        loggedInUsers.append(data)
        return recommend_animes_by_genres_only(data["genres"], age=data["isOver18"], type=data["movieShow"])
    else:
        return "User already exists, try logging in"
    
@app.post('/login')
def login():
    data = request.json
    
    for user in loggedInUsers:
        if data['username'] == user['username'] and data['password'] == user['password']:
            print("data['username']: ", data['username'])
            #return "Logged In"
            return recommend_animes_for_user(data['username'], k=5)
    return "user does not exist!"


if __name__ == '__main__':
    app.run()
    