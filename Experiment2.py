import spotipy
from spotipy.oauth2 import SpotifyOAuth ##idk if this is really needed
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64


CLIENT_ID = 'd576e9eb16044adbaa2d22688fc73dd0'
CLIENT_SECRET = '7b5cc4d0a7ce40ee9f8c0ea42aba241b'

#do a lookup for a token
#this token is for future requests

AUTH_URL = 'https://accounts.spotify.com/api/token'
#token_url

method = 'POST'
token_data = {
    'grant_type': 'client_credentials',
}
token_header = {
    'Authorization':
}







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

export SPOTIPY_CLIENT_ID='d576e9eb16044adbaa2d22688fc73dd0'
export SPOTIPY_CLIENT_SECRET='7b5cc4d0a7ce40ee9f8c0ea42aba241b'
#export SPOTIPY_REDIRECT_URI='your-app-redirect-url


auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)
