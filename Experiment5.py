import os, sys, json, webbrowser
import spotipy
import lyricsgenius
import pandas as pd
import spotipy.util as util
from json.decoder import JSONDecodeError


#Get the username from terminal
username = sys.argv[1]

#User ID: g64129687775 (mine)
#Genius accces token: cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io


#Type these into to terminal before running:
# set SPOTIPY_CLIENT_ID=d576e9eb16044adbaa2d22688fc73dd0
# set SPOTIPY_CLIENT_SECRET=7b5cc4d0a7ce40ee9f8c0ea42aba241b
# set SPOTIPY_REDIRECT_URI=https://www.google.co.uk/
# set GENIUS_ACCESS_TOKEN=cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io
#   <<IMPORTANT: Change URI to your webapp address>>



#Erase cache and prompt

try:
    token = util.prompt_for_user_token(username, scope='user-read-recently-played user-top-read' )

except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']


#Create our objects
spotifyObject = spotipy.Spotify(auth=token)
geniusObject = lyricsgenius.Genius(genius_access_token)


#This prints out json data in a format that we can read
#print(json.dumps(VARIABLE, sort_keys=True, indent=4))


#Returns user's recently played
results = spotifyObject.current_user_recently_played(limit=50, after=None, before=None)
recents = results['items']
while results['next']:
    results = spotifyObject.next(results)
    recents.extend(results['items'])


songs = []
for recent in recents:
    features = spotifyObject.audio_features(recent['track']['id'])[0]
    song = geniusObject.search_song(title=recent['track']['name'], artist=recent['track']['artists'][0]['name'])


    try:
        songs.append({
            'name' : recent['track']['name'],
            'artists' : [d['name'] for d in recent['track']['artists']],
            #'features' : features,
            'acousticness' : features['acousticness'],
            'danceability' : features['danceability'],
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
            'played at' : recent['played_at'],
            'lyrical_data' : song.lyrics
        })
    except:
        songs.append({
            'name' : recent['track']['name'],
            'artists' : [d['name'] for d in recent['track']['artists']],
            #'features' : features,
            'acousticness' : features['acousticness'],
            'danceability' : features['danceability'],
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
            'played at' : recent['played_at'],
            'lyrical_data' : None
        })

df = pd.DataFrame(songs)
print(df)
#print(json.dumps(songs, sort_keys=True, indent=4))
