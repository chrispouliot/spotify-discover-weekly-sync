from gpm import GPM
from spotify import Spotify


class MusicClient(object):
    _client = None

    def get_playlist(self, name):
        '''
        Retrieve a playlist from the music client

        :param str name: The name of the playlist to retrieve
        :return: The playlist
        :rtype: Playlist serializer object
        '''
        return self._client.get_playlist(name)

    def create_playlist(self, playlist, override_existing=True):
        '''
        Create a playlist from the music client

        :param playlist: The playlist to be created
        :type playlist: Playlist serializer object
        :param bool override_existing: Delete playlist if it already exists
        :return: Number of songs matched
        :rtype: Int
        '''
        return self._client.create_playlist(playlist, override_existing)


class SpotifyClient(MusicClient):
    _client = Spotify()


class GPMClient(MusicClient):
    _client = GPM()
