import spotipy

class SpotifyAPI:

    def __init__(self, token=None, redirect_uri=None) -> None:
        # Initialise Spotify object for the retrieval of user data
        self.spotify_object = spotipy.Spotify(auth=token) if token else None
        self.client_id = 'd576e9eb16044adbaa2d22688fc73dd0'
        self.scope = 'user-read-recently-played user-top-read user-read-private user-read-email'
        self.open_browser=True # Has to be true to allow other users to logout
        self.auth_manager = self.get_auth_manager(redirect_uri=redirect_uri)


    def get_auth_manager(self, redirect_uri, client_id=None):
        # Suppose to use the PKCE package but not really sure
        return spotipy.oauth2.SpotifyPKCE(
                    client_id = self.client_id, 
                    redirect_uri = redirect_uri, 
                    scope = self.scope, 
                    open_browser=self.open_browser) 


    # Convert time played into date and time formats
    def convert_date_time(self, timestamp):
        date = timestamp[0:10]
        time = timestamp[11:16]
        return time, date


    # Return song as a dictionary
    def get_song_dict(self, song) -> dict:
        # Get song id, name and artist(s)
        track_id = song['track']['id']
        track_name = song['track']['name']
        track_artists = song['track']['artists']

        # Get features
        features = self.spotify_object.audio_features(track_id)[0]

        # Create song dictionary
        song_dict = {'name' : track_name, 'artists' : [d['name'] for d in track_artists]}

        # Find time song was played for chonological ordering
        song_dict['datetime'] = self.convert_date_time(song['played_at']),

        # Add song features to dictionary
        for feat in features.keys():
            song_dict[feat] = features[feat]

        return song_dict
    


    # Get user data from Spotify for model predictions
    def get_user_songs(self) -> list:
        
        # Return user's recently played songs
        results = self.spotify_object.current_user_recently_played(limit=50, after=None, before=None)
        
        # Convert songs into a list
        recents = results['items']
        while results['next']:
            results = self.spotify_object.next(results)
            recents.extend(results['items'])

        # Return song data as a list of dictionaries    
        return [self.get_song_dict(x) for x in recents]
