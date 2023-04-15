from flask import Flask, request, jsonify
# from recommend_anime import recommend_animes_based_on_search, search_animes, preprocess_title_and_genre, df_anime, model, user_mapping, anime_mapping
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import pandas as pd
import torch
import torch.nn as nn
class MatrixFactorization(nn.Module):
    def __init__(self, n_users, n_anime, n_factors):
        super(MatrixFactorization, self).__init__()
        self.user_factors = nn.Embedding(n_users, n_factors)
        self.anime_factors = nn.Embedding(n_anime, n_factors)

    def forward(self, user, anime):
        return (self.user_factors(user) * self.anime_factors(anime)).sum(1)
# Load the model
mapping_dict = torch.load('C:/Users/vigne/OneDrive/Documents/WPI/Sem_2/IR/project/mapping.pth')
user_mapping = mapping_dict['user_mapping']
anime_mapping = mapping_dict['anime_mapping']
n_factors=100
model = MatrixFactorization(len(user_mapping), len(anime_mapping), n_factors)
model.load_state_dict(torch.load('C:/Users/vigne/OneDrive/Documents/WPI/Sem_2/IR/project/model.pth'))
model.eval()

# Load mappings and DataFrame

df_anime = pd.read_csv('C:/Users/vigne/OneDrive/Documents/WPI/Sem_2/IR/project/archive/animes.csv')
df_anime = df_anime[['uid', 'title', 'genre']].rename(columns={'uid': 'anime_id'})

def recommend_animes_based_on_search(model, df_anime, user_mapping, anime_mapping, query, user_id=None, N=10):
    if user_id is None:
        user_idx = len(user_mapping) - 1
    else:
        user_idx = user_mapping[user_id]

    # Search for animes based on the query
    searched_animes = search_animes(df_anime, query)

    if searched_animes.empty:
        print("No animes found matching the search query.")
        return searched_animes

    # Get the indices of the searched animes
    searched_anime_indices = [anime_mapping.get(anime_id) for anime_id in searched_animes['anime_id'].values if anime_id in anime_mapping]

    if not searched_anime_indices:
        print("No matching animes found in the anime_mapping.")
        return pd.DataFrame()

    # Get scores for the searched animes
    user_tensor = torch.tensor([user_idx] * len(searched_anime_indices), dtype=torch.long)
    anime_tensor = torch.tensor(searched_anime_indices, dtype=torch.long)
    anime_scores = model(user_tensor, anime_tensor)

    # Get top N recommended anime indices and their respective anime IDs
    top_N_indices = torch.topk(anime_scores, min(N, len(searched_anime_indices))).indices
    top_N_anime_ids = [list(anime_mapping.keys())[list(anime_mapping.values()).index(idx)] for idx in top_N_indices.tolist()]

    # Filter the searched animes based on the top N recommendations
    recommended_anime = searched_animes[searched_animes['anime_id'].isin(top_N_anime_ids)].reset_index(drop=True)

    return recommended_anime

def preprocess_title_and_genre(df_anime):
    df_anime['title_processed'] = df_anime['title'].str.lower().str.replace('[^\w\s]', '')
    df_anime['genre_processed'] = df_anime['genre'].str.lower().str.replace('[^\w\s]', '').fillna('')
    df_anime['title_genre'] = df_anime['title_processed'] + ' ' + df_anime['genre_processed']
preprocess_title_and_genre(df_anime)
def search_animes(df_anime, query, top_n=10, similarity_threshold=0.2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_anime['title_genre'])

    query_vector = vectorizer.transform([query.lower()])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    top_n_indices = cosine_similarities.argsort()[-top_n:][::-1]

    # Filter indices based on the similarity threshold
    top_n_indices = [idx for idx in top_n_indices if cosine_similarities[idx] > similarity_threshold]

    if not top_n_indices:
        return pd.DataFrame()

    searched_animes = df_anime.iloc[top_n_indices].reset_index(drop=True)

    return searched_animes

app = Flask(__name__)

@app.route('/search_animes', methods=['GET'])
def search_animes_route():
    search_query = request.args.get('query')
    searched_animes = search_animes(df_anime, search_query)
    return jsonify(searched_animes.to_dict(orient='records'))

@app.route('/recommend_animes', methods=['GET'])
def recommend_animes_route():
    search_query = request.args.get('query')
    user_id = int(request.args.get('user_id'))
    N = int(request.args.get('N', 10))
    recommended_anime = recommend_animes_based_on_search(model, df_anime, user_mapping, anime_mapping, search_query, user_id, N)
    return jsonify(recommended_anime.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
