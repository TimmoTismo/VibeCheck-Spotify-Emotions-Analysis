import os, sys, json, webbrowser
import spotipy
import lyricsgenius
import pandas as pd
import nltk
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def main():
    #Get the username from terminal
    username = 'g64129687775'
    #username = sys.argv[1]
    #User ID: 
    #   g64129687775 (mine)
    #   itsjessbrookes
    #Genius accces token: cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io


    #Type these into to terminal before running:
    # set SPOTIPY_CLIENT_ID=d576e9eb16044adbaa2d22688fc73dd0
    # set SPOTIPY_CLIENT_SECRET=7b5cc4d0a7ce40ee9f8c0ea42aba241b
    # set SPOTIPY_REDIRECT_URI=https://www.google.co.uk/
    # set GENIUS_ACCESS_TOKEN=cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io
    #   <<IMPORTANT: Change URI to your webapp address>>

    
    client_id = 'd576e9eb16044adbaa2d22688fc73dd0'
    client_secret = '7b5cc4d0a7ce40ee9f8c0ea42aba241b'
    redirect_uri = 'http://localhost/'
    scope='user-read-recently-played user-top-read user-read-private user-read-email'

    #Erase cache and prompt
    # try:
    #     token = util.prompt_for_user_token(username, scope='user-read-recently-played user-top-read' )

    # except:
    #     os.remove(f".cache-{username}")
    #     token = util.prompt_for_user_token(username)
    try:
        os.remove(f".cache-{username}")
        token = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope,username=username,show_dialog=True)
    except:
        token = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope,username=username,show_dialog=True)

    #genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']
    genius_access_token = 'cQ15SgX_iCubNYTUW2pivTNrZbHmUIBHlzUHg2GEbDbrFUmzEVaRFE9BPvefe2io'

    #Create our objects
    spotifyObject = spotipy.Spotify(auth_manager=token)
    geniusObject = lyricsgenius.Genius(genius_access_token)

    analyser = SentimentIntensityAnalyzer()


    #This prints out json data in a format that we can read
    #print(json.dumps(VARIABLE, sort_keys=True, indent=4))


    #Returns user's recently played
    results = spotifyObject.current_user_recently_played(limit=50, after=None, before=None) #This line opens up a page in the browser
    
    recents = results['items']
    while results['next']:
        results = spotifyObject.next(results)
        recents.extend(results['items'])


    songs = []
    for recent in recents:
        features = spotifyObject.audio_features(recent['track']['id'])[0]
        song = geniusObject.search_song(title=recent['track']['name'], artist=recent['track']['artists'][0]['name'])


        if song:
            try:
                lyric_score = analyser.polarity_scores(song.to_text())
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
                    'played_at' : recent['played_at'],
                    'lyrics' : song.lyrics,
                    'nlp_lyrics' : lyric_score['compound'],
                    'valence+nlp' : round(features['valence']+lyric_score['compound']/100, 4)
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
                    'played_at' : recent['played_at'],
                    'lyrics' : song.lyrics,
                    'nlp_lyrics' : None
                })
        else:
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
                'played_at' : recent['played_at'],
                'lyrics' : None,
                'nlp_lyrics' : None
            })

    df = pd.DataFrame(songs)
    print(df[['name', 'artists', 'valence','energy', 'nlp_lyrics','valence+nlp', 'played_at']])
    #print(json.dumps(songs, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()