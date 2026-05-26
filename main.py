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


def get_features(track_name):
    r = df[df["track_name"] == track_name].iloc[0]


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



def get_recommendations_euclid_genre_filtering(temp_df, result, weights):
    
    result = np.multiply(result, weights)

    euclid_dist = np.linalg.norm(result.astype(np.float64), axis = 1)

    top = np.argpartition(euclid_dist, 5)[:5]

    top = top[np.argsort(euclid_dist[top])]  # sort just the 5

    # print(temp_df.iloc[top]["track_name"])

    return temp_df.iloc[top].index


df = pd.read_csv("data1.csv")

lis = ["danceability",
              "energy", 
              "valence",
              "acousticness",
              "speechiness",
              "instrumentalness",
              "liveness",
              "tempo",
              ]


df = normalise_data(df, lis)

artists = ("Enter artist:")
track_name = ("Enter the name of the track:")

track_name = "Stairway to Heaven - Remaster"
artists = "Led Zeppelin"

row = df[(df["track_name"] == track_name) & (df["artists"] == artists)]

# print(df)

track_genre = row.values[0][-1]

# no more genre filtering
# row = df[df["track_id"] == id].iloc[0]
# track_genre = row["track_genre"]

# filter

temp_df = df[(df["track_genre"] == track_genre) & (df["track_name"] != track_name)]

# nomralise and get original track features normalised

track_features = df[(df["track_name"] == track_name) & (df["artists"] == artists)][lis]


original = np.array(track_features)
features_matrix = np.array(temp_df[lis].values)
result = np.array(features_matrix - original)
ranks = np.zeros(len(df), dtype=np.int32)


for j in range(1):

    weights = np.random.uniform(0, 3, size = 8)

    weights /= weights.sum()

    ans = get_recommendations_euclid_genre_filtering(temp_df, result, weights)

    ranks[ans] += 1

top = np.argpartition(ranks, -5)[-5:]
# print(ranks[top])

for i in top:
    recsong = df.iloc[i]["track_name"]
    recartist = df.iloc[i]["artists"]
    print(recsong, "by", recartist)

    
