import os, sys, json, webbrowser, pprint
import spotipy 
import lyricsgenius
import pandas as pd
import nltk
import spotipy.util as util
import spotipy.oauth2 as oauth2
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from requests.exceptions import Timeout


def get_playlist_tracks(playlist_id):
    results = spotifyObject.playlist(playlist_id)['tracks']
    playlist = results['items']
    while results['next']:
        results = spotifyObject.next(results)
        playlist.extend(results['items'])
    return playlist


# Define variables
username = 'g64129687775'
client_id = 'd576e9eb16044adbaa2d22688fc73dd0'
client_secret = '7b5cc4d0a7ce40ee9f8c0ea42aba241b'
redirect_uri = 'http://localhost/'
scope='user-read-recently-played'

# Create tokens
token = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope,username=username,show_dialog=True)
genius_access_token = 'cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io'

# Create API objects
spotifyObject = spotipy.Spotify(auth_manager=token)
geniusObject = lyricsgenius.Genius(genius_access_token)

tracks = get_playlist_tracks('37i9dQZF1DX76Wlfdnj7AP')
#playlist = spotifyObject.playlist('spotify:playlist:37i9dQZF1DWTC99MCpbjP8')

geniusObject.timeout = 15

# for x in playlist['tracks']['items']:
#     track_id = x['track']['id']
#     track_name = x['track']['name']
#     track_artists = x['track']['artists']
#     print(track_name)
for x in tracks:
    print(x['track']['name'])


