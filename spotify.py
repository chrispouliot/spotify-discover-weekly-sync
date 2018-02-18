import logging
import os
import requests

from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

from serializers import Playlist

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
USER_ID = os.environ.get("SPOTIFY_USER_ID")

BASE_URL = "https://api.spotify.com/v1"
AUTHORIZE_URL = "https://accounts.spotify.com/api/token"
PLAYLISTS_URL = f"https://api.spotify.com/v1/users/{USER_ID}/playlists"


class Spotify(object):
    _granted_token = ""
    _token_expiry_date = datetime.now()

    def _get_auth(self, re_auth=False):

        if self._token_expiry_date > datetime.now() and not re_auth:
            return self._granted_token

        self._granted_token, self._token_expiry_date = self._authenticate()
        return self._granted_token

    def _authenticate(self):
        data = {
            "grant_type": "client_credentials"
        }

        r = requests.post(AUTHORIZE_URL, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), data=data)

        if r.status_code >= 400:
            raise Exception("Something bad status {} {}".format(r.status_code, r.text))

        body = r.json()
        expiry = body.get("expires_in")
        token = body.get("access_token")

        if not expiry or not token:
            logging.warning(
                "Failed to authenticate with Spotify. Invalid tokens returned. Status code %s",
                r.status_code
            )
            raise Exception("Unable to fulfill your request")

        token_expiry = datetime.now() + timedelta(seconds=expiry)

        return token, token_expiry

    def _get(self, url):
        token = self._get_auth()
        headers = {"Authorization": "Bearer {token}".format(token=token)}

        r = requests.get(url, headers=headers)

        if r.status_code >= 400:
            raise Exception("Something bad status {} {}".format(r.status_code, r.text))

        return r.json()

    def get_playlist(self, name):
        user_playlists = self._get(PLAYLISTS_URL)
        playlist = None

        # TODO: Handle pagination of results
        for user_playlist in user_playlists['items']:
            if user_playlist['name'] == name:
                playlist = user_playlist
                break

        if not playlist:
            logging.warning("Unable to find playlist '{}'. Is it public?".format(name))
            return None

        # Exchange the minified playlist for a full playlist
        playlist = self._get(playlist['href'])

        # Once we've found the playlist, get all it's tracks
        next_results_url = playlist['tracks']['next']

        # Spotify paginates long results
        while next_results_url:
            paginated_results = self._get(next_results_url)
            next_results_url = paginated_results['next']

            playlist['tracks']['items'] += paginated_results['items']

        return Playlist.from_spotify(playlist)

    def create_playlist(self, playlist_obj, override):
        return None
