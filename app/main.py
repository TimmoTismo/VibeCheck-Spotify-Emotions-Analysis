from flask import Flask, render_template, redirect, request, session
import os, json, secrets, time

from statistics import mode

import pandas as pd
import pickle

#from model_class import Spotify API Class created
from app.spotify_api_class import SpotifyAPI

from spotipy.oauth2 import SpotifyPKCE

# CONSTANTS
app = Flask(__name__)

ssk = secrets.token_hex(16)
app.secret_key = ssk




@app.route('/')
def index():
    return redirect('home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about') # Might need to change this
def about():
    return render_template('about.html')

@app.route('/error')
def error():
    return render_template('error.html')


# Source: https://stackoverflow.com/questions/57580411/storing-spotify-token-in-flask-session-using-spotipy
# authorization-code-flow Step 1. Have your application request authorization; 
# the user logs in and authorizes access
@app.route("/login")
def login():
    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    auth_manager = SpotifyAPI(redirect_uri=get_redirect_uri()).auth_manager


    # Get User Authorisation URL for this app
    auth_url = auth_manager.get_authorize_url()
    #print('auth_url: ',auth_url)

    # Send user to Spotify authorisation page
    return redirect(auth_url)



# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens
@app.route("/api_callback")
def api_callback():
    # Not sure if this is needed
    #session.clear()

    # Retrieve response code from URL
    code = request.args.get('code')
    #print('code: ', code)

    # If user clicks 'Cancel'
    if not code:
        return redirect('home')


    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    auth_manager = SpotifyPKCE(client_id='d576e9eb16044adbaa2d22688fc73dd0', 
                               redirect_uri=get_redirect_uri(), 
                               scope='user-read-recently-played user-top-read user-read-private user-read-email')

    #print(auth_manager.get_authorization_code(request.url))

    # Add access token to sessions
    token_info = auth_manager.get_access_token(code)

    # Saving the access token along with all other token related info
    session["token_info"] = token_info

    # Send user to loading page
    return redirect('loading')

@app.route("/loading")
def loading():
    return render_template("loading.html")


# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data
@app.route("/results", methods=['GET', 'POST'])
def results():
    session['token_info'], authorized = validate_token(session)
    session.modified = True

    if not authorized:
        return redirect('/home')
    

    # Call model to predict on user's data
    results, user_data = predict()
    
    # Calculate user's most prevalent mood
    user_mood = mode(results)

    # Reverses order of index
    user_data = user_data.iloc[::-1].reset_index()
    user_data = user_data.drop(columns='index')
    # print(json.dumps(response))
    # user_data returns a dataframe

    ## TODO: Add more graphs
    valence = user_data['valence'].tolist()
    energy = user_data['energy'].tolist()

    # Counting labelled frequencies of each mood
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
    
    # Appending results to user_data dataframe
    user_data['predicted mood'] = results

    return render_template("dashboard.html", user_mood=user_mood, user_data=user_data, valence=valence, energy=energy, distribution=json.dumps(distribution))


@app.route("/logout")
def logout():
    try:    
        # Remove the CACHE file (.cache-test) so that a new user can login.
        os.remove('.cache')
        session.clear()
    except:
        pass
    return redirect('home')


# Returns redirect URI depending on root URL
# This makes it so that I don't have to manually change the redirect URI everytime I switch between production and development servers
def get_redirect_uri():
    return request.url_root + 'api_callback'


# Checks to see if token is valid and gets a new token if not
def validate_token(session):
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
        
        auth_manager = SpotifyAPI(redirect_uri=get_redirect_uri()).auth_manager
            
        token_info = auth_manager.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid





# Retrieve model predictions
def predict():
    # Load in saved model
    clf = pickle.load(open('models/model.sav', 'rb'))


    #Initialise
    sp_api = SpotifyAPI(token=session.get('token_info').get('access_token'), 
                        redirect_uri=get_redirect_uri())
    
    # Getting songs from user
    songs = sp_api.get_user_songs()

    # Storing data in dataframe
    user_data = pd.DataFrame(songs)

    # Drop unnecessary columns
    user = user_data.drop(columns=['duration_ms','datetime'])
    X_test = user.iloc[:, 2:13]
    
    # Rearrange columns in right order
    cols = X_test.columns.tolist()
    cols.sort()
    X_test = X_test[cols]


    # Predict
    # svm_predictions = svm_model_linear.predict(X_test)
    svm_predictions = clf.predict(X_test)
    
    
    return svm_predictions, user_data