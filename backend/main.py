from flask import Flask, request, jsonify
import requests
from models.user import User
import json
from flask_cors import CORS
from util.coldStart import recommend_animes_by_genres_only

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

loggedInUsers = [{'username': 'amey', 'password': 'amey', 'genres': ['Action', 'Comedy', 'Drama', 'Horror'], 'isOver18': '24', 'movieShow': 'Show'}]

topRecommendedAnime = []


@app.route('/')
def hello():
    return 'Hello, World!'

@app.post('/register')
def register():
    data = request.json
    # process the data
    print("Data: ", type(data['isOver18']))

    if data not in loggedInUsers:
        loggedInUsers.append(data)
        print("LoggedInUsers: ", loggedInUsers)
        #Run recommendation function using user details
        #return "Registered successfully"
        return recommend_animes_by_genres_only(data["genres"], age=data["isOver18"], type=data["movieShow"])
    else:
        return "User already exists, try logging in"
    
@app.post('/login')
def login():
    data = request.json
    # process the data
    print("data['password']:", data['password'])
    
    for user in loggedInUsers:
        if data['username'] == user['username'] and data['password'] == user['password']:
            return "user logged in successfully"
    return "user does not exist"

    


if __name__ == '__main__':
    app.run()
    