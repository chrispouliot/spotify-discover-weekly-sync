from gpm import GPM
from spotify import Spotify


class MusicClient(object):
    _client = None

    def get_playlist(self, name):
        return self._client.get_playlist(name)

    def create_playlist(self, playlist_obj):
        return self._client.create_playlist(playlist_obj)


class SpotifyClient(MusicClient):
    _client = Spotify()


class GPMClient(MusicClient):
    _client = GPM()
