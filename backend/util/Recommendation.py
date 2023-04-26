import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.sparse import csr_matrix, save_npz, load_npz


animes = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/animes.csv')
profiles = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/profiles.csv')
reviews = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/reviews.csv')

animes = animes.drop_duplicates(subset=['title'], keep='first')

import re
def get_genre_score(user_favorite_genres):
    genre_columns = [col for col in animes.columns if col in user_favorite_genres]
    genre_scores = animes[genre_columns].sum(axis=1)
    return genre_scores
# Step 2: Feature engineering (simplified for this example)
def extract_genres(genre_str):
    if isinstance(genre_str, str):
        return re.findall(r"\w+\s?\w*", genre_str)
    else:
        return []

animes['genres'] = animes['genre'].apply(extract_genres)
mlb = MultiLabelBinarizer()
genres_encoded = mlb.fit_transform(animes['genres'])
genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_)
animes = pd.concat([animes.drop(['genres'], axis=1), genres_df], axis=1)

scaler = MinMaxScaler()
animes[['ranked', 'popularity', 'score']] = scaler.fit_transform(animes[['ranked', 'popularity', 'score']])

# Fill NaN values with zeros
animes_copy=animes.copy()
animes_cleaned = animes.drop(['title', 'synopsis', 'genre', 'aired', 'img_url', 'link'], axis=1).fillna(0)

similarity_matrix = cosine_similarity(animes_cleaned)

def get_anime_id(title):
    anime_df = animes[animes['title'] == title]
    if not anime_df.empty:
        return anime_df.index[0]
    else:
        return None

def get_anime_title(anime_id):
    return animes.iloc[anime_id]['title']

def recommend_animes_by_titles(user_favorite_titles, k=10):
    user_favorites_ids = [get_anime_id(title) for title in user_favorite_titles]
    user_favorites_ids = [x for x in user_favorites_ids if x is not None]  # Remove any None values
    user_similarities = np.sum(similarity_matrix[user_favorites_ids], axis=0)
    top_k_indices = user_similarities.argsort()[-k-1:][::-1]
    top_k_indices = [idx for idx in top_k_indices if idx not in user_favorites_ids][:k]
    
    return [get_anime_title(idx) for idx in top_k_indices]


# Your specified genres array
genres_18_above = ['Hentai', 'Ecchi', 'Haren','Yuri','Yaoi']

# Function to check if any genre from the array is in the anime genres
def is_18_above(genre_str):
    if isinstance(genre_str, str):
        for genre in genres_18_above:
            if genre in genre_str:
                return 1
            return 0

# Add the '18_above' column to the animes DataFrame
animes['18_above'] = animes['genre'].apply(is_18_above)

# Display the updated animes DataFrame
print(animes['18_above'].value_counts())

animes = animes[animes['18_above'] == 0].reset_index(drop=True)

# COLD START

def recommend_animes_by_genres_only(user_favorite_genres, k=10, age=None, type=None):
    genre_scores = get_genre_score(user_favorite_genres)

    valid_animes = animes.copy()

    if age is not None and age < 18:
        valid_animes = valid_animes[valid_animes['18_above'] == 0]

    if type == 'movie':
        valid_animes = valid_animes[valid_animes['episodes'] == 1]
    elif type == 'series':
        valid_animes = valid_animes[valid_animes['episodes'] > 1]

    genre_scores = pd.Series(genre_scores, index=animes.index)
    genre_scores = genre_scores.loc[valid_animes.index]

    top_k_indices = genre_scores.nlargest(k).index

    return [get_anime_title(idx) for idx in top_k_indices]


user_favorites_genres = ['Vampire', 'Horror', 'Demons']
user_age = 16
type_anime='movie'


recommendations = recommend_animes_by_genres_only(user_favorites_genres, age=user_age,type=type_anime)


# USER BASED COLLABORATIVE FILTERING

user_item_matrix = reviews.pivot_table(index='profile', columns='anime_uid', values='score')
#sparse_user_item_matrix = csr_matrix(user_item_matrix.fillna(0))
#user_similarity_matrix_sparse = cosine_similarity(sparse_user_item_matrix, dense_output=False)
#save_npz('user_similarity_matrix_sparse1.npz', user_similarity_matrix_sparse)


loaded_user_similarity_matrix_sparse = load_npz('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/user_similarity_matrix_sparse.npz')




def find_k_similar_users(user, k=16):
    user_index = user_item_matrix.index.get_loc(user)
    user_similarities = loaded_user_similarity_matrix_sparse[user_index].toarray().flatten()
    
    # Ignore the similarity score of the user with themselves
    user_similarities[user_index] = -1
    
    top_k_indices = user_similarities.argsort()[-k:][::-1]
    top_k_users = [user_item_matrix.index[idx] for idx in top_k_indices]
    top_k_scores = user_similarities[top_k_indices]
    
    return top_k_users, top_k_scores


def recommend_animes_for_user(user, k=16):
    similar_users, similar_users_scores = find_k_similar_users(user, k)
    similar_users_preferences = user_item_matrix.loc[similar_users].fillna(0)
    weighted_preferences = similar_users_preferences.mul(similar_users_scores, axis=0)
    user_preferences = weighted_preferences.sum(axis=0) / similar_users_scores.sum()
    
    # Ignore animes the user has already rated
    user_rated_animes = user_item_matrix.loc[user].dropna().index
    user_preferences[user_rated_animes] = -1
    
    top_k_indices = user_preferences.argsort()[-k:][::-1]
    top_k_animes = []
    for anime_id in top_k_indices:
        anime_df = animes[animes['uid'] == anime_id]
        if not anime_df.empty:
            top_k_animes.append(anime_df.iloc[0]['title'])
    
    # Fill empty slots with top animes based on rating
    top_animes = animes.sort_values(by='score', ascending=False)['title'].tolist()
    for i in range(k):
        if i >= len(top_k_animes) or top_k_animes[i] == '':
            for anime_title in top_animes:
                if anime_title not in top_k_animes:
                    top_k_animes.append(anime_title)
                    break
    
    return top_k_animes[:k]


