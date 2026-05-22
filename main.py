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


def get_recommendations_euclid(df, id, track_name, features_list):

    original = np.array(get_features(id).values)

    features_matrix = np.array(df[features_list].values)

    result = np.array(features_matrix - original)

# Force the data type to float64 before computing the norm

    euclid_dist = np.linalg.norm(result.astype(np.float64), axis = 1)

    df["results"] = euclid_dist

    df = df.sort_values(by="results", ascending=True)

    ans = set()
    # print(len(ans))

    for i in df.itertuples():
        if (i.track_id == id or i.track_name == track_name):
            continue
        else:
            ans.add((i.track_name, i.artists))
        
        if (len(ans) == 5):
            break
    
    return ans

    # for i in collection.itertuples():
    #     print(i)

    # for j in collection:
        # print(j[1])

    # result = []

    # c = 0

    # for i in features_matrix:
    #     k = np.linalg.norm(np.subtract(i, original))
    #     result.append(k)

    # df["results"] = result

    # ans = []

    # for i in df.itertuples():
    #     ans.append((i.results, (i.track_name, i.artists)))

    # ans.sort(reverse = True)
    # while (ans[-1][0] == 0):
    #     ans.pop()

    # final = [ans[-1]]
    # last_track = ans[-1][1][0]

    # while (len(final)<5):
    #     if (ans[-1][1][0] != last_track):
    #         final.append(ans[-1])
    #         last_track = ans[-1][1][0]



    # for i in features_matrix:
    #     i -= original


    # df["euclid_dist"] = np.linalg.norm(df["recommendation_vectors"] - original)

        

    


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


artists = "Imagine Dragons"
track_name = "Demons"

id = get_id(artists, track_name)

track_features = get_features(id)

ans = get_recommendations_euclid(df, id, track_name, lis)

for i in ans:
    print(i[0], "by", i[1])

# for i in ls:
#     print(i[1][0], "by", i[1][1])

# for i in ls:
#     id = i[1]
#     row = df[df["track_id"] == id]
#     song = row.iloc[0]
#     print(song["track_name"], "by", song["artists"])

# # for i in ls:
# #     row = df[df["track_id"] == i[1]].iloc[0]
#     print(row["track_name"])



