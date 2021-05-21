# Importing necessary libraries
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import math




X_train, y_train = getModelValues()

# Training a linear SVM classifier
from sklearn.svm import SVC
svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)

# Get user data from Spotify as the X_test variable
#username = 'g64129687775' #learn how to pass the username in

# Create tokens
#token = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope,username=username,show_dialog=True)
genius_access_token = 'cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io'

# Create API objects
#spotifyObject = spotipy.Spotify(auth_manager=token)
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
for x in recents:
    track_id = x['track']['id']
    track_name = x['track']['name']
    track_artists = x['track']['artists']
    
    annotation = None
    lyric_score = None
    annotation_score = None
    
    features = spotifyObject.audio_features(track_id)[0]

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
        
        # Genius features
        # 'lyrics' : song.lyrics if song else None,
        # 'annotations' : annotation if annotation else None,
        'nlp_lyrics' : lyric_score['compound'] if lyric_score else None,
        'nlp_annotations' : annotation_score['compound'] if annotation_score else None,
        
        'valence+nlp' : round(features['valence']+(lyric_score['compound']+annotation_score['compound'])/100, 4) if song else features['valence']
        })
    except Exception as e:
        print('############################')
        print(e)
        print('Error 2 For', track_name)
        print('############################')



user_data = pd.DataFrame(songs)

# Drop unnecessary columns
user = user_data.drop(columns=['duration_ms', 'nlp_lyrics', 'nlp_annotations'])

X_test = user.iloc[:, 2:15]

# Predict
svm_predictions = svm_model_linear.predict(X_test)