import spotipy
from spotipy.oauth2 import SpotifyOAuth ##idk if this is really needed
import requests


CLIENT_ID = 'd576e9eb16044adbaa2d22688fc73dd0'
CLIENT_SECRET = '7b5cc4d0a7ce40ee9f8c0ea42aba241b'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '6y0igZArWVi6Iz0rj35c1Y'

# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

r = r.json()
print(r)




#########################################
# scope = "user-library-read"
#
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
#
# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
