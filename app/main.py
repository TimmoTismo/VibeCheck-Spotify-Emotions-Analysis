from flask import Flask, render_template, redirect, request, session, make_response, url_for, render_template_string
import spotipy 



app = Flask(__name__)

@app.route('/')
def index():
    return redirect('home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove('.cache')
        session.clear()
    except:
        pass

    # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, scope = scope, show_dialog=show_dialog)
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)

    return redirect(auth_url)
