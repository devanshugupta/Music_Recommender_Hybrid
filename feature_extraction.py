import os
import librosa
import numpy as np
import csv
import scipy
from scipy import stats

'''
NOTE: notation for MODE: MAJOR =0.1, MINOR =0.9, MAJMIN =1, Maj or Min =0
'''

header = 'song mood album artist1 artist2 artist3 harmonic percussion tempo zcr spec_bw spec_cent rolloff rmse chroma mel tonnetz'
for i in range(1, 21):
    header += f' mfcc{i}'

header = header.split()

excel = open('H:/song_metadata.csv', 'a', newline='')
with excel:
    writer = csv.writer(excel)
    writer.writerow(header)


note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def key(X):
    X = scipy.stats.zscore(X)

    major = np.asarray([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    major = scipy.stats.zscore(major)

    minor = np.asarray([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    minor = scipy.stats.zscore(minor)

    # Generate all rotations of major
    major = scipy.linalg.circulant(major)
    minor = scipy.linalg.circulant(minor)

    major, minor = major.T.dot(X), minor.T.dot(X)
    major, minor = np.median(major,axis=1), np.median(minor,axis=1)
    major_winner = int(np.argmax(major))
    minor_winner = int(np.argmax(minor))
    # essentia adds a 0.5? why
    # https://github.com/MTG/essentia/blob/master/src/algorithms/tonal/key.cpp#L370

    if major[major_winner] > minor[minor_winner]:
        return major_winner, 0.1
    elif major[major_winner] < minor[minor_winner]:
        return minor_winner, 0.9
    else:
        if major_winner == minor_winner:
            return major_winner, 1
        else:
            return major_winner, 0



for file in os.listdir(f'H:/hindisongs'):

    d_file = open('artist.txt')
    with d_file:
        d_text = d_file.read()
    g_file = open('mood.txt')
    with g_file:
        g_text = g_file.read()
    al_file = open('album.txt')
    with al_file:
        al_text = al_file.read()

    d, g, al = eval(d_text), eval(g_text), eval(al_text)
    c, c1, c2 = len(d), len(g), len(al)

    for filename in os.listdir(f'H:/hindisongs/{file}'):
        singer1,singer2,singer3 = 0,0,0
        try:
            audio = f'H:/hindisongs/{file}/{filename}'
            audio_duration = librosa.get_duration(filename=audio)
            duration, offset = audio_duration // 2, audio_duration // 3
            y, sr = librosa.load(audio, duration=duration, offset=offset)

            rmse = librosa.feature.rms(y=y)
            chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
            zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))
            spec_cent = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spec_bw = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
            rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            mel = np.mean(librosa.feature.melspectrogram(y, sr=sr))
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            percussion = librosa.effects.percussive(y, margin=8)

            harmonic = librosa.effects.harmonic(y, margin=8)
            chromagram = librosa.feature.chroma_cqt(y=harmonic, sr=sr)
            note, mode = key(chromagram)


            ##Beat_srength & Tempo
            onset_env = librosa.onset.onset_strength(y, sr=sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, aggregate=None)

            ##Power & Loudness
            S = librosa.stft(y, center=False)
            power = np.abs(S) ** 2
            p_mean = np.sum(power, axis=0, keepdims=True)
            p_ref = np.max(power)  # or whatever other reference power you want to use
            loudness = librosa.power_to_db(p_mean, ref=p_ref)
            
            tonnetz = np.mean(librosa.feature.tonnetz(y=harmonic, sr=sr))

            #Artist, Title, Album extraction
            filename = filename.split('-')
            artist = filename[0]
            song = filename[1]
            if len(filename)>2:
                album = filename[2]
            else:
                album = song
            artist = artist.split(',')
            album = album[:-4]
            song, album = song.strip(), album.strip()
            album, song = album.lower(), song.lower()
            song = song.replace(' ', '_')

            if ' ' in album:
                album = album.replace(' ', '_')

            for ind, i in enumerate(artist):

                i = i.strip().lower()

                if i not in d:
                    c += 1
                    d[i] = c
                if ind == 0:
                    singer1 = d[i]
                elif ind == 1:
                    singer2 = d[i]
                elif ind == 2:
                    singer3 = d[i]
                else:
                    pass
            if '"' in album:
                album = album.split('"')[1]
            album = album.replace(' ', '_')
            if album not in al:
                c2 += 1
                al[album] = c2

            #Append to .csv file
            to_append = f'{song} {str(file)} {al[album]} {singer1} {singer2} {singer3} {note} {mode} {np.mean(harmonic)} {np.mean(percussion)} {loudness} {np.mean(tempo)} {np.mean(onset_env)} {zcr} {spec_bw} {spec_cent} {rolloff} {np.mean(rmse)} {chroma} {mel} {tonnetz}'
            for i in mfcc:
                to_append += f' {np.mean(i)}'

            excel = open('H:/song_metadata.csv', 'a', newline='')
            with excel:
                writer = csv.writer(excel)
                writer.writerow(to_append.split())
        except Exception as e:
            print(filename, e)


    d_file = open('artist.txt', 'w')
    with d_file:
        d_file.write(str(d))
    g_file = open('mood.txt', 'w')
    with g_file:
        g_file.write(str(g))
    al_file = open('album.txt', 'w')
    with al_file:
        al_file.write(str(al))

    d_file.close()
    g_file.close()
    al_file.close()
