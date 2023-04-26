import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def display(user):
# Load and process data
    df_anime = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/animes.csv')
    df_reviews = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/reviews.csv')
    df_anime = df_anime[['uid', 'title','img_url','link','genre']]
    df_anime.rename(columns={'uid': 'anime_id'}, inplace=True)
    df_anime = df_anime.drop_duplicates()

    print("df_review.column: ", df_reviews.columns)

    df_reviews_cp = df_reviews[['profile', 'anime_uid', 'score']]
    df_reviews_cp = df_reviews_cp[df_reviews_cp['score'] != -1]
    df_reviews_cp['score'] = df_reviews_cp['score'] / 10  # Scale the scores to the range of 0 to 5
    df_reviews_cp = df_reviews_cp.sample(frac=1).reset_index(drop=True)
    

# Map user and anime ids to integer indices
    user_mapping = {user_id: idx for idx, user_id in enumerate(df_reviews_cp.profile.unique())}
    anime_mapping = {anime_id: idx for idx, anime_id in enumerate(df_reviews_cp.anime_uid.unique())}


    df_reviews_cp['user_id'] = df_reviews_cp['profile'].apply(lambda x: user_mapping[x])
    df_reviews_cp['anime_id'] = df_reviews_cp['anime_uid'].apply(lambda x: anime_mapping[x])


    def is_18_above(genre_str):
        genres_18_above = ['Hentai', 'Ecchi', 'Harem', 'Yuri', 'Yaoi']
        if isinstance(genre_str, str):
            for genre in genres_18_above:
                if genre in genre_str:
                    return 1
            return 0

    df_anime['18_above'] = df_anime['genre'].apply(is_18_above)

# Define neural network-based item similarity and rating prediction model
    class ItemSimilarityAndRating(nn.Module):
        def __init__(self, n_users, n_anime, n_factors):
            super(ItemSimilarityAndRating, self).__init__()
            self.user_factors = nn.Embedding(n_users, n_factors)
            self.anime_factors = nn.Embedding(n_anime, n_factors)

        def similarity(self, anime1, anime2):
            dot_product = (self.anime_factors(anime1) * self.anime_factors(anime2)).sum(1)
            return dot_product

        def rating(self, user, anime):
            dot_product = (self.user_factors(user) * self.anime_factors(anime)).sum(1)
            return torch.sigmoid(dot_product) * 10  # Scale the predicted ratings to the range of 0 to 5

# Initialize model, loss function, and optimizer
    n_users = len(user_mapping)
    n_anime = len(anime_mapping)
    n_factors = 200
    model = ItemSimilarityAndRating(n_users, n_anime, n_factors)
    loss_func = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loaded_model = ItemSimilarityAndRating(n_users, n_anime, n_factors)
    loaded_model.load_state_dict(torch.load('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/item_similarity_and_rating_model.pth'))
    loaded_model.eval()


# Get top 10 similar animes
    anime_id = 1  # Change this to the ID of the anime you want to find similar animes for
    anime_index = anime_mapping[anime_id]
    anime_tensor = torch.tensor([anime_index] * n_anime, dtype=torch.long)
    other_anime_tensor = torch.tensor(list(range(n_anime)), dtype=torch.long)

    anime_similarities = loaded_model.similarity(anime_tensor, other_anime_tensor)

# Get top 11 similar animes
    top_11_indices = torch.topk(anime_similarities, 11).indices

    top_10_indices = top_11_indices[1:]

    top_10_anime_ids = [list(anime_mapping.keys())[list(anime_mapping.values()).index(idx)] for idx in top_10_indices.tolist()]
    recommended_anime = df_anime[df_anime['anime_id'].isin(top_10_anime_ids)].reset_index(drop=True)
    recommended_anime = recommended_anime[recommended_anime['18_above'] == 0].reset_index(drop=True)
    top_10_similarities = anime_similarities[top_10_indices].tolist()
    # print("Top 10 Similar Animes and Similarity Scores:")
    # for idx, row in recommended_anime.iterrows():
    #     print(f"{row} (Similarity Score: {top_10_similarities[idx]:.2f})")
    


# Predict ratings (top 10 animes) for a user
    user_id = user  # Change this to the user ID for which you want to predict ratings
    user_index = user_mapping[user_id]
    user_tensor = torch.tensor([user_index] * n_anime, dtype=torch.long)

    predicted_ratings = loaded_model.rating(user_tensor, other_anime_tensor)

    unique_anime_ids = df_reviews_cp['anime_uid'].unique()
    unique_animes_df = df_anime[df_anime['anime_id'].isin(unique_anime_ids)].reset_index(drop=True)
    predicted_ratings_df = pd.DataFrame({'title': unique_animes_df['title'], 'predicted_rating': predicted_ratings.tolist()})

    predicted_ratings_df = predicted_ratings_df.sort_values(by='predicted_rating', ascending=False).head(10)


# Predict ratings (all animes) for a user
    unique_anime_ids = df_reviews_cp['anime_uid'].unique()
    unique_animes_df = df_anime[df_anime['anime_id'].isin(unique_anime_ids)].reset_index(drop=True)
    n_unique_anime = len(unique_anime_ids)

# Create user_tensor and other_anime_tensor for unique animes
    user_tensor_unique = torch.tensor([user_index] * n_unique_anime, dtype=torch.long)
    other_anime_tensor_unique = torch.tensor(list(range(n_unique_anime)), dtype=torch.long)

# Predict ratings for unique animes
    predicted_ratings_unique = loaded_model.rating(user_tensor_unique, other_anime_tensor_unique)

# Create a dataframe with predicted ratings for unique animes
    predicted_ratings_df = pd.DataFrame({'title': unique_animes_df['title'], 'predicted_rating': predicted_ratings_unique.tolist()})
    predicted_ratings_df['predicted_rating'] = predicted_ratings_df['predicted_rating'].apply(round)

    return recommended_anime[['title', 'img_url', 'link']].to_dict('records')


