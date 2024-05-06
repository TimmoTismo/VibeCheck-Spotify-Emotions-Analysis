import spotipy, requests, sys
from spotipy.oauth2 import SpotifyPKCE
from spotify_api_class import SpotifyAPI



redirect_uri='http://127.0.0.1:5000/api_callback'


auth_manager = SpotifyAPI(redirect_uri=redirect_uri).auth_manager


token = auth_manager.get_access_token()


sp =  spotipy.Spotify(auth=token)


results = sp.current_user_recently_played(limit=50, after=None, before=None)


print(results)
