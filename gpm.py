from gmusicapi import Mobileclient

from config import GPM_APP_PASSWORD, GPM_EMAIL_ADDRESS
from utils import is_match
from serializers import Playlist


class GPM(object):
    _api = None

    def __init__(self):
        self._api = Mobileclient(debug_logging=False)
        if not self._api.login(GPM_EMAIL_ADDRESS, GPM_APP_PASSWORD, Mobileclient.FROM_MAC_ADDRESS):
            raise Exception("Failed to authenticate with GPM")

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
            if is_match(hit['title'], song.title) and is_match(hit['artist'], song.artist):
                return hit['storeId']

        return None
    
    def _get_playlist(self, name):
        playlists = self._api.get_all_user_playlist_contents()
        for playlist in playlists:
            if playlist['name'] == name:
                return playlist
        return None

    def get_playlist(self, name):
        playlist = self._get_playlist(name)
        return Playlist.from_gpm(playlist) if playlist else None

    def create_playlist(self, playlist, override):
        gpm_playlist = self._get_playlist(playlist.title)
        gpm_playlist_id = gpm_playlist['id'] if gpm_playlist else None

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
