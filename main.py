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


def get_recommendations(df, id):
    ls = []
    original = np.array(get_features(id).values)  # O(N)
    c = 0
    distinct_songs = {"null"}

    for i in df.itertuples():
        # print(i[0], i[1], i[2], i[3])

        if i.track_id == id:
            continue

        rec = [i.danceability, i.energy, i.valence, i.acousticness, i.speechiness, i.instrumentalness, i.liveness, i.tempo]
        # df["vectors"] = [i[9], i[10]]

        if (np.linalg.norm(original) == 0 or np.linalg.norm(rec) == 0):
            continue

        cos_sim = original @ rec / (np.linalg.norm(original) * np.linalg.norm(rec))

        if i.track_name in distinct_songs:
            continue
        else:
            ls.append((cos_sim, (i.track_name, i.artists), cos_sim))
            distinct_songs.add(i.track_name)

    ls.sort(reverse = True)

    return ls[0:5]




        

    


df = pd.read_csv("archive/dataset.csv")
''' Unnamed: 0', 'track_id', 'artists', 'album_name', 'track_name',
       'popularity', 'duration_ms', 'explicit', 'danceability', 'energy',
       'key', 'loudness', 'mode', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature',
       'track_genre'],
'''
# c=0
# for i in df:
#     print(i)
#     if c < 10:
#         c+= 1
#     else:
#         break

lis = ["danceability",
              "energy", 
              "valence",
              "acousticness",
              "speechiness",
              "instrumentalness",
              "liveness",
              "tempo"]

df = normalise_data(df, lis)


artists = "Radiohead"
track_name = "Creep"

id = get_id(artists, track_name)

track_features = get_features(id)


ls = get_recommendations(df, id)

for i in ls:
    print(i[1][0], "by", i[1][1], "\nsimilarity:", i[2])

# for i in ls:
#     id = i[1]
#     row = df[df["track_id"] == id]
#     song = row.iloc[0]
#     print(song["track_name"], "by", song["artists"])

# # for i in ls:
# #     row = df[df["track_id"] == i[1]].iloc[0]
#     print(row["track_name"])



