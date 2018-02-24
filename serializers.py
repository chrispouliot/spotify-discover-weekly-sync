class Song(object):
    title = ''
    artist = ''
    album = ''

    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

    def __repr__(self):
        return f"Song<{self.title} - {self.artist}>"

    @staticmethod
    def from_spotify(json):
        return Song(
            title=json['name'],
            artist=json['artists'][0]['name'],  # Just take the first artist
            album=json['album']['name'],
        )
    
    @staticmethod
    def from_gpm(json):
        return Song(
            title=json['title'],
            artist=json['artist'],
            album=json['album'],
        )


class Playlist(object):
    songs = []
    title = ''
    description = ''

    def __init__(self, songs, title, description):
        self.songs = songs
        self.title = title
        self.description = description

    def __repr__(self):
        return f"Playlist<{self.title}>"

    @staticmethod
    def from_spotify(json):
        return Playlist(
            songs=[Song.from_spotify(item['track']) for item in json['tracks']['items']],
            title=json['name'],
            description=json['description'],
        )
    
    @staticmethod
    def from_gpm(json):
        return Playlist(
            songs=[Song.from_gpm(item['track']) for item in json['tracks']],
            title=json['name'],
            description=json['description'],
        )
