import os

from gmusicapi import Mobileclient

EMAIL_ADDRESS = os.environ.get('GPM_EMAIL_ADDRESS')
APP_PASSWORD = os.environ.get('GPM_APP_PASSWORD')


class GPM(object):
    _api = None

    def __init__(self):
        self._api = Mobileclient(debug_logging=False)
        if not self._api.login(EMAIL_ADDRESS, APP_PASSWORD, Mobileclient.FROM_MAC_ADDRESS):
            raise Exception("Failed to authenticate with GPM")

    def _get_playlist(self, name):
        playlists = self._api.get_all_playlists()
        for playlist in playlists:
            if playlist['name'] == name:
                return playlist
        return None

    def _delete_playlist(self, playlist_id):
        return self._api.delete_playlist(playlist_id)

    def _create_playlist(self, name, description):
        return self._api.create_playlist(name, description)

    def _add_songs_to_playlist(self, playlist_id, song_ids):
        return self._api.add_songs_to_playlist(playlist_id, song_ids)
    
    def _match_song(self, song):
        query = f'{song.title} {song.artist}'
        results = self._api.search(query)

        hits = [song_hit['track'] for song_hit in results.get('song_hits')]
        # Check if song is a match
        for hit in hits:
            title, artist, album = hit['title'], hit['artist'], hit['album']
            # TODO: Make this smarter
            if song.title in title and song.artist in artist:
                return hit['storeId']

        return None

    def get_playlist(self, name):
        return None

    def create_playlist(self, playlist, override):
        gpm_playlist_id = self._get_playlist(playlist.title).get('id')
        # Delete if it already exists
        if gpm_playlist_id and override:
            self._delete_playlist(gpm_playlist_id)
        # Create it if we are re-making it or it didn't already exist
        if not gpm_playlist_id or override:
            gpm_playlist_id = self._create_playlist(playlist.title, playlist.description)

        # Get all song_ids and remove results we could not match
        matches = [self._match_song(song) for song in playlist.songs]
        song_ids = [match for match in matches if match is not None]
        
        self._add_songs_to_playlist(gpm_playlist_id, song_ids)
        # Return number of songs added to playlist
        return len(song_ids)