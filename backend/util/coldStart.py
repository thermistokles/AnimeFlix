import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MultiLabelBinarizer

# Step 1: Load and preprocess the data
animes = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/animes.csv')
profiles = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/profiles.csv')
reviews = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/reviews.csv')

animes = animes.drop_duplicates(subset=['title'], keep='first')

import re

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

def get_genre_score(user_favorite_genres):
    genre_columns = [col for col in animes.columns if col in user_favorite_genres]
    genre_scores = animes[genre_columns].sum(axis=1)
    return genre_scores

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

def get_anime_details(anime_ids):
    anime_details = []
    
    for anime_id in anime_ids:
        anime_df = animes[animes['uid'] == anime_id]
        
        if not anime_df.empty:
            title = anime_df.iloc[0]['title']
            img_url = anime_df.iloc[0]['img_url']
            score = anime_df.iloc[0]['score']
            anime_details.append((title, img_url, score*5))
    
    return anime_details

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

    top_k_animes = get_anime_details(top_k_indices)
    
    return top_k_animes

