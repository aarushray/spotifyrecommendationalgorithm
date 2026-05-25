from dotenv import load_dotenv

import os # os.getenv gets client id
import requests # for making POST request to get access token
import base64 # encoding authorization string
import json
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_id(artists, track_name):
    r = df[(df["artists"] == artists) & (df["track_name"] == track_name)]
    return r["track_id"].iloc[0]


def get_features(id):
    r = df[df["track_id"] == id].iloc[0]
    return r[["danceability",
              "energy", 
              "valence",
              "acousticness",
              "speechiness",
              "instrumentalness",
              "liveness",
              "tempo"]]

def normalise_data(df, list1):

    for i in list1:
        
        low = df[i].min()
        high = df[i].max()
        denominator = high - low

        if denominator == 0:
            df[i] = 0
        else:
            df[i] = (df[i] - low)/denominator

    return df


def get_recommendations_cos(df, id):
    ls = []
    original = np.array(get_features(id).values)  # O(N)
    c = 0
    distinct_songs = {"null"}

    for i in df.itertuples():

        if i.track_id == id:
            continue

        rec = [i.danceability, i.energy, i.valence, i.acousticness, i.speechiness, i.instrumentalness, i.liveness, i.tempo]

        if (np.linalg.norm(original) == 0 or np.linalg.norm(rec) == 0):
            continue

        cos_sim = original @ rec / (np.linalg.norm(original) * np.linalg.norm(rec))

        if i.track_name in distinct_songs:
            continue
        else:
            ls.append((cos_sim, (i.track_name, i.artists)))
            distinct_songs.add(i.track_name)

    ls.sort(reverse = True)

    return ls[0:5]


def get_recommendations_euclid_genre_filtering(temp_df, result, weights):
    
    result = np.multiply(result, weights)

    euclid_dist = np.linalg.norm(result.astype(np.float64), axis = 1)

    top = np.argpartition(euclid_dist, 5)[:5]

    top = top[np.argsort(euclid_dist[top])]  # sort just the 5

    row_numbers = temp_df.iloc[top]["Unnamed: 0"]

    return row_numbers


df = pd.read_csv("history-of-rock-spotify - Copy.csv")

lis = ["danceability",
              "energy", 
              "valence",
              "acousticness",
              "speechiness",
              "instrumentalness",
              "liveness",
              "tempo"]

df = normalise_data(df, lis)


artists = ("Enter artist:")
track_name = ("Enter the name of the track:")

artists = "Radiohead"
track_name = "Creep"


id = get_id(artists, track_name)

track_features = get_features(id).values

row = df[df["track_id"] == id].iloc[0]
track_genre = row["track_genre"]
temp_df = df[(df["track_genre"] == track_genre) & (df["track_name"] != track_name)]
temp_df = temp_df.drop_duplicates(subset="track_name")

original = np.array(track_features)
features_matrix = np.array(temp_df[lis].values)
result = np.array(features_matrix - original)
ranks = np.zeros(len(df), dtype=np.int32)

for j in range(1000):

    weights = np.random.uniform(0, 3, size = 8)

    weights /= weights.sum()

    ans = get_recommendations_euclid_genre_filtering(temp_df, result, weights)


    ranks[ans] += 1

top = np.argpartition(ranks, 5)[-5:]

for i in top:
    recsong = df.iloc[i]["track_name"]
    recartist = df.iloc[i]["artists"]
    print(recsong, "by", recartist)

    
