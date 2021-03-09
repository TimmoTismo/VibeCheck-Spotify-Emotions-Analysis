import os, sys, json, webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

#Get the username from terminal
username = sys.argv[1]

#User ID: g64129687775 (mine)


#Type these into to terminal before running:
# set SPOTIPY_CLIENT_ID=d576e9eb16044adbaa2d22688fc73dd0
# set SPOTIPY_CLIENT_SECRET=7b5cc4d0a7ce40ee9f8c0ea42aba241b
# set SPOTIPY_REDIRECT_URI=https://www.google.co.uk/
#   <<IMPORTANT: Change URI to your webapp address>>


#Erase cache and prompt

try:
    token = util.prompt_for_user_token(username, scope='user-read-recently-played user-top-read' )

except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)


#Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)


#This prints out json data in a format that we can read
#print(json.dumps(VARIABLE, sort_keys=True, indent=4))


# #Print user's information
# user = spotifyObject.current_user()
# print(json.dumps(user, sort_keys=True, indent=4))
#
#
# #Print artists albums:
# joji_uri = 'spotify:artist:3MZsBdqDrRTJihTHQrO6Dq'
# results = spotifyObject.artist_albums(joji_uri, album_type='album')
# print(json.dumps(results, sort_keys=True, indent=4))
# #===========================================
# #Print albums out in a list
# albums = results['items']
# while results['next']:
#     results = spotifyObject.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])
# #===========================================



#Returns user's recently played
results = spotifyObject.current_user_recently_played(limit=50, after=None, before=None)
recents = results['items']
while results['next']:
    results = spotifyObject.next(results)
    recents.extend(results['items'])


# for recent in recents:
#     trackId = recent['track']['id']
#     trackName = recent['track']['name']
#     strArtists = ''
#     for artist in recent['track']['artists']:
#         strArtists += artist['name'] + ', '
#     print('Track:', trackName + '\nArtists:', strArtists + '\nTrack ID:', trackId)
#     print('###############################################')


# trackIds = []
# for recent in recents:
#     trackIds.append(recent['track']['id'])
#
# features = spotifyObject.audio_features(trackIds)
# for feature in features:
#     print(feature['valence'])

#print(json.dumps(features, sort_keys=True, indent=4))


songs = []
for recent in recents:
    features = spotifyObject.audio_features(recent['track']['id'])[0]
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
        '_played at' : recent['played_at']
    })
print(json.dumps(songs, sort_keys=True, indent=4))
