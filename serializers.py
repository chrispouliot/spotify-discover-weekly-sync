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
    description = ''

    def __init__(self, songs, title, description):
        self.songs = songs
        self.title = title
        self.description = description

    @staticmethod
    def from_spotify(json):
        return Playlist(
            songs=[Song.from_spotify(item['track']) for item in json['tracks']['items']],
            title=json['name'],
            description=json['description'],
        )
