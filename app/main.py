#from flask import Flask, render_template, redirect, url_for
from flask import Flask, render_template, redirect, request, session, make_response, url_for
import requests

import os, sys, json, webbrowser, pprint, time, secrets
import spotipy 
import lyricsgenius
import nltk
import spotipy.util as util
import spotipy.oauth2 as oauth2 ######## This line and lie 4 might cause issues
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from requests.exceptions import Timeout

# from rq import Queue
# from worker import conn

# Importing necessary libraries for model
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import math
import matplotlib.pyplot as plt
from statistics import mode
from datetime import datetime


app = Flask(__name__)

nltk.download('vader_lexicon')
ssk = secrets.token_hex(16)
app.secret_key = ssk

client_id = 'd576e9eb16044adbaa2d22688fc73dd0'
client_secret = '7b5cc4d0a7ce40ee9f8c0ea42aba241b'
# redirect_uri = 'https://vibecheck1.herokuapp.com/api_callback'
redirect_uri = 'http://127.0.0.1:5000/api_callback'
scope='user-read-recently-played user-top-read user-read-private user-read-email'

show_dialog=True #Has to be true to allow other users to logout

API_BASE = 'https://accounts.spotify.com'



# Model functions
def getModelValues():
    # Read data
    data = pd.read_csv('datasets/data.csv')
    
    # Pre-process the data

    # Remove the index column from csv file
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')] 

    # Drop unnecessary columns
    df = data.drop(columns=['duration_ms', 'nlp_lyrics', 'nlp_annotations'])

    # Randomise rows
    df = df.sample(frac=1).reset_index(drop=True)

    X_train = df.iloc[:, 2:15] # All rows, features only, no labels
    y_train = df.iloc[:, 15] # All rows, label only, no features

    return X_train, y_train

def convertDateTime(timestamp):
    date = timestamp[0:10]
    time = timestamp[11:16]
    return time, date

def getSongs(spotifyObject):
    # Get user data from Spotify as the X_test variable
    
    # Create tokens
    genius_access_token = 'cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io'
    
    # Create API objects
    geniusObject = lyricsgenius.Genius(genius_access_token)
    geniusObject.timeout = 15

    # Create NLP analyser
    analyser = SentimentIntensityAnalyzer()

    results = spotifyObject.current_user_recently_played(limit=50, after=None, before=None) #This line opens up a page in the browser

    recents = results['items']
    while results['next']:
        results = spotifyObject.next(results)
        recents.extend(results['items'])


    songs = []
    #x is items
    for x in recents:
        track_id = x['track']['id']
        track_name = x['track']['name']
        track_artists = x['track']['artists']
        
        annotation = None
        lyric_score = None
        annotation_score = None
        
        features = spotifyObject.audio_features(track_id)[0]

        # Uncomment this section to use nlp =================================
        retries = 0
        while retries < 3:
            try:
                song = geniusObject.search_song(title=track_name, artist=track_artists[0]['name'])
            except Timeout as e:
                retries += 1
                continue            
            break


        try:
            annotation = geniusObject.song_annotations(song.id)
            lyric_score = analyser.polarity_scores(song.to_text())
            annotation_score = analyser.polarity_scores(song.to_text())
        except Exception as e:
            print('############################')
            print(e)
            print('Error 1 For', track_name)
            print('############################')
        #=================================================================

        try:
            songs.append({
            # Spotify features
            'name' : track_name,
            'artists' : [d['name'] for d in track_artists],
            'acousticness' : features['acousticness'],
            'danceability' : features['danceability'],
            'duration_ms' : features['duration_ms'],
            'energy' : features['energy'],
            'instrumentalness' : features['instrumentalness'],
            'key' : features['key'],
            'liveness' : features['liveness'],
            'loudness' : features['loudness'],
            'mode' : features['mode'],
            'speechiness' : features['speechiness'],
            'tempo' : features['tempo'],
            'time_signature' : features['time_signature'],
            'valence' : features['valence'],
            'played_at' : x['played_at'],
            'datetime' : convertDateTime(x['played_at']),

            # Genius features
            # 'lyrics' : song.lyrics if song else None,
            # 'annotations' : annotation if annotation else None,

            # Uncomment these to use nlp
            'nlp_lyrics' : lyric_score['compound'] if lyric_score else None,
            'nlp_annotations' : annotation_score['compound'] if annotation_score else None,
            'valence+nlp' : round(features['valence']+(lyric_score['compound']+annotation_score['compound'])/100, 4) if song else features['valence']
            })
        except Exception as e:
            print('############################')
            print(e)
            print('Error 2 For', track_name)
            print('############################')
            
    return songs

def predict(spotifyObject):
    X_train, y_train = getModelValues()

    # Training a linear SVM classifier
    from sklearn.svm import SVC
    svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)

    # from rq import Queue
    # from worker import conn

    # q = Queue(connection=conn)  

    # songs = q.enqueue(getSongs, spotifyObject)
    songs = getSongs(spotifyObject)

    user_data = pd.DataFrame(songs)

    # Drop unnecessary columns
    user = user_data.drop(columns=['duration_ms','played_at', 'datetime', 'nlp_lyrics', 'nlp_annotations'])
    X_test = user.iloc[:, 2:15]
    
    # w/o nlp
    # user = user_data.drop(columns=['duration_ms','played_at', 'datetime'])
    # X_test = user.iloc[:, 2:13]

    # Predict
    svm_predictions = svm_model_linear.predict(X_test)

    return svm_predictions, user_data

@app.route('/')
def index():
    return redirect('home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/error')
def error():
    return render_template('error.html')


# Checks to see if token is valid and gets a new token if not
def get_token(session):
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
        sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = scope, show_dialog=show_dialog)
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

# authorization-code-flow Step 1. Have your application request authorization; 
# the user logs in and authorizes access
@app.route("/login")
def login():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove('.cache')
        session.clear()
    except:
        pass

    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = scope, show_dialog=show_dialog)
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)

    return redirect(auth_url)

# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens
@app.route("/api_callback")
def api_callback():
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = scope, show_dialog=show_dialog)
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    # Saving the access token along with all other token related info
    session["token_info"] = token_info


    return redirect("results")

# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data
@app.route("/results", methods=['GET', 'POST'])
def results():
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        return redirect('/')
    data = request.form
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results, user_data = predict(sp)
    r = mode(results)

    # Reverses order of index
    user_data = user_data.iloc[::-1].reset_index()
    user_data = user_data.drop(columns='index')
    # print(json.dumps(response))
    # user_data returns a dataframe
    valence = user_data['valence'].tolist()
    energy = user_data['energy'].tolist()

    distribution = {
        'Happy' : results.tolist().count('Happy'),
        'Sad' : results.tolist().count('Sad'),
        'Calm' : results.tolist().count('Calm'),
        'Sleepy' : results.tolist().count('Sleepy'),
        'Energised' : results.tolist().count('Energised'),
        'Aroused' : results.tolist().count('Aroused'),
        'Angry' : results.tolist().count('Angry'),
        'Chill' : results.tolist().count('Chill'),
    }

    return render_template("dashboard.html", data=data, r=r, user_data=user_data, valence=valence, energy=energy, distribution=json.dumps(distribution))


@app.route("/logout")
def logout():
    try:    
        # Remove the CACHE file (.cache-test) so that a new user can login.
        os.remove('.cache')
        session.clear()
    except:
        pass
    return redirect('home')



