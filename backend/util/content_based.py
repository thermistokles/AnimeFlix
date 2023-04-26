import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rake_nltk import Rake
from sklearn.metrics.pairwise import linear_kernel
import pickle

# load the anime dataset
dataset = pd.read_csv('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/preprocessedForContent.csv')
# initialize the RAKE algorithm and compute the keywords
rake = Rake()
keywords = []

# check if the vectorized bag of words file exists
try:
    with open('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/vectorized_bag_of_words.pkl', 'rb') as f:
        vectorized_bag_of_words = pickle.load(f)
except:
    # initialize the vectorizer and compute the vectorized bag of words
    vectorizer = CountVectorizer()
    vectorized_bag_of_words = vectorizer.fit_transform(dataset['bag of words'])

    # store the vectorized bag of words in a file
    with open('A:/study_material/WPI/SEM2/IR/FinalProject/AnimeFlix/backend/util/vectorized_bag_of_words.pkl', 'wb') as f:
        pickle.dump(vectorized_bag_of_words, f)

dataset = dataset.reset_index(drop=True)

def recommend(show_title, n_recom, age):
    # find the index of the target show in the dataset
    target_show = dataset[dataset['title'] == show_title]
    
    # Check if the target show exists in the dataset
    if target_show.empty:
        print(f"{show_title} not found in the dataset.")
        return []

    target_index = target_show.index[0]

    # compute the pairwise cosine similarities between the target show and all the other shows
    similarities = linear_kernel(vectorized_bag_of_words, vectorized_bag_of_words[target_index].reshape(1, -1))

    # sort the similarities in descending order
    sorted_indices = np.argsort(similarities.squeeze())[::-1]

    # initialize an empty list of recommendations
    recommendations = []

    # iterate through the sorted indices and add recommendations based on the age filter
    count = 0
    for index in sorted_indices:
        if count >= n_recom:
            break

        # Skip the current index if the title is the same as the show_title
        if dataset.loc[index, "title"] == show_title:
            continue

        if age < 18 and dataset.loc[index, 'adult']:
            continue
        else:
            recommendations.append({"title": dataset.loc[index, "title"], "image_url": dataset.loc[index, "img_url"], "link": dataset.loc[index, "link"]})
            count += 1

    return recommendations
