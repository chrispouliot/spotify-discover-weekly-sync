from flask import Flask, redirect, render_template
from musicsync import SpotifyOAuth

from server.config import \
    SPOTIFY_CLIENT_ID, \
    REDIRECT_URL

# Server static through nginx in future
app = Flask(__name__, template_folder="client", static_folder="client")


@app.route('/')
def index():
    return redirect(SpotifyOAuth.get_oauth_url(SPOTIFY_CLIENT_ID, REDIRECT_URL, ''))


@app.route('/callback')
def callback():
    return render_template('index.html')
