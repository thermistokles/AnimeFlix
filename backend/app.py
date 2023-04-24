from flask import Flask, request, jsonify,json
from flask_cors import CORS
from test1 import recommend_animes_based_on_search, search_animes, filter_animes_by_age, preprocess_title_and_genre, df_anime
from Recommendation import recommend_animes_for_user, find_k_similar_users, recommend_animes_for_user,find_k_similar_users,loaded_user_similarity_matrix_sparse,recommend_animes_by_genres_only,is_18_above,recommend_animes_by_titles,get_anime_title,animes_copy,get_anime_id,extract_genres,get_genre_score
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#https://stackoverflow.com/a/10434709/11441843
@app.route('/', methods=['POST'])
# def search():
#     request_data = request.data.decode('utf-8')
#     return f"name passed: {request_data}"
#     request_json = json.loads(request_data)
#     search_text = request_json['searchText']
#     response_data = f"Search query received: {search_text}"
#     return response_data
#     #return f"name passed: {search_text}"
#     '''if request.method == 'POST':
#         request_data = request.json
#         return jsonify(request_data)
#     else:
#         return "Send a POST request with JSON data to this endpoint."'''

def search():
    if request.method == 'POST':
        request_data = request.json
        print("Request data ",request_data)
        search_query = request_data['searchText']
        user_id = 43
        N = 20
        user_age = 21
        restricted_genres = ['Hentai', 'Ecchi', 'Harem', 'Yuri', 'Yaoi']
        searched_animes = search_animes(df_anime, search_query, N)
        searched_animes = filter_animes_by_age(searched_animes, user_age, restricted_genres)
        response_data = searched_animes[['anime_id', 'title','img_url','link']].to_dict('records')
        
        return jsonify(response_data)
    else:
        return "Send a POST request with JSON data to this endpoint."

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    user = 'edgewalker00'
    recommendations = recommend_animes_for_user(user)
    recommended_anime_df = animes_copy[animes_copy['title'].isin(recommendations)]
    response_data = recommended_anime_df[['title', 'img_url', 'link']].to_dict('records')
    return jsonify(response_data)


@app.route('/ucf',methods=['GET'])
def ucf():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body

@app.route('/')
def hello():
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)

    '''
    most safe aproach is probably to run "Set-ExecutionPolicy Unrestricted -Scope Process", 
    that would allow you to run virtualenv in current powershell session '''