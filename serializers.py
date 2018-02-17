class Song(object):
    title = ''
    artist = ''
    album = ''

    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

    @staticmethod
    def from_spotify(json):
        # Just take the first artist
        artist = json['artists'][0].get('name', '')
        album = json['album'].get('name', '')
        title = json.get('name', '')
        return Song(
            title=title,
            artist=artist,
            album=album,
        )


class Playlist(object):
    songs = []
    title = ''

    def __init__(self, songs, title):
        self.songs = songs
        self.title = title

    @staticmethod
    def from_spotify(json):
        return Playlist(
            songs=[Song.from_spotify(song) for song in json['tracks']],
            title=json['name'],
        )
