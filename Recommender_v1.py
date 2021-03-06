"""
    Title: Recommender system
    File Name: Recommender_v1.py
    Author: Devanshu Gupta
    Language: Python
    Date Modified: 17-07-2020
    ##########################################################################################################
    # Description:
    #       Content based Recommender system with Similar artist filter as middle layer in architecture.
    #       Similarity is calculated based on song features and user history.
    #
    #       Files necessary : Similar_Artist.txt, file2.csv
    # Weight list is updated for every user depending on songs liked.
    ##########################################################################################################
"""
from typing import List, Any, Union

import pandas as pd
import numpy as np
import math
from heapq import nlargest, nsmallest
from sklearn.preprocessing import MinMaxScaler, minmax_scale

df = pd.read_csv('file2.csv')
df.set_index('song_id', inplace=True)
users = pd.read_csv('users.csv', index_col='username')

cols = ['harmonic', 'percussion', 'tempo', 'zcr',
        'spec_bw', 'spec_cent', 'rolloff', 'rmse', 'chroma', 'mel', 'tonnetz',
        'mfcc1', 'mfcc2', 'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6', 'mfcc7', 'mfcc8',
        'mfcc9', 'mfcc10', 'mfcc11', 'mfcc12', 'mfcc13', 'mfcc14', 'mfcc15',
        'mfcc16', 'mfcc17', 'mfcc18', 'mfcc19', 'mfcc20', 'loudness',
        'onset_env']

scaler = MinMaxScaler()

df[cols] = scaler.fit_transform(df[cols])

ptr = open('Similar_Artist.txt')
with ptr:
    text = ptr.read()
similar_artist = eval(text)

weight = [0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.3, 0.3, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          0.2, 0.2]

def recommend(song_set, username):
    users = pd.read_csv('users.csv', index_col='username')
    if users.loc[username].sum() > 50:
        songs = users.loc[username].to_numpy().nonzero()
        songs = df.loc[songs]
        songs = songs.iloc[:, 11:]
        var = songs.var()
        weight = minmax_scale(var)

    f = open('song_id.txt')
    with f as file:
        txt = file.read()
    songs = eval(txt)
    l = []
    for i in song_set:
        l.append(songs[i])
    recommendations = get_recommendation(l)
    return recommendations

def get_recommendation(songs_set):
    # main function for recommender system
    final_recommendation = []
    similarity_dict = {}
    for song in songs_set:
        rec_song = get_similar(song)
        similarity_dict = cosine_similarity(song, rec_song)
        final_recommendation += top_K_songs(similarity_dict, k=2)
    final_recommendation=list(set(final_recommendation))

    return final_recommendation


def get_similar(song_id):
    rec_song, sim_artist = [], []

    mood_of_song = (df.loc[song_id]['mood'])  # Find mood of song
    artist_of_song = [x for x in list(df.loc[song_id][4:6]) if
                      str(x) != '0']  # Extracting artist and removing nan values in list
    data = df[df['mood'] == mood_of_song]  # making dataframe of respective mood

    for a in artist_of_song:
        a = a.replace('_', ' ')
        if a not in similar_artist[mood_of_song.lower().strip()]:
            continue

        sim_artist += similar_artist[mood_of_song.lower().strip()][
            a]  # get similar artist (for each artist) list from Similar_Artist.
    sim_artist = [x.lower() for x in sim_artist]

    for same in sim_artist:  # looping through similar artist to get respective songs.
        if (data.artist_1 == same).any():
            rec_song += data[data['artist_1'] == same].index.to_list()
        if (data.artist_2 == same).any():
            rec_song += data[data['artist_2'] == same].index.to_list()

    if song_id in rec_song:
        rec_song.remove(song_id)

    if rec_song == []:  # No song found in database...
        for a in artist_of_song:  # Recommend song from the same artists.
            if (data.artist_1 == a).any():
                rec_song += data[data['artist_1'] == a].index.to_list()
            if (data.artist_2 == a).any():
                rec_song += data[data['artist_2'] == a].index.to_list()

    rec_song = list(set(rec_song))  # Remove duplicate index...

    # rec_song += data[data['artist_1']==a].index.to_list()
    # rec_song = rec_song + data[data['artist_2']==a].index.to_list()
    return rec_song


def get_feature(song_id):
    return df.loc[song_id][11:]


def cosine_similarity(song_id, rec_song):
    similarity_dict = {}
    dot_product = []
    listen_song = np.array(get_feature(song_id))
    for s in rec_song:
        song = np.array(get_feature(s))
        dot_product = [a * b for a, b in zip(listen_song, song)]
        dot_product = [a / (b+1) for a, b in zip(dot_product, weight)]
        similarity_dict[s] = sum(dot_product)
    return similarity_dict  # return dictionary {song_id : similarity_value} in this format..

def top_K_songs(dict, k):
    return nlargest(k, dict, key=dict.get)
