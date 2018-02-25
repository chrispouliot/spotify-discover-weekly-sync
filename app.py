import sys

from datetime import datetime

from config import logger
from musicclient import GPMClient, SpotifyClient


def main(playlist_titles):
    spotify = SpotifyClient()
    gpm = GPMClient()

    for title in playlist_titles:
        logger.info(f"Attempting to copy playlist '{title}'..")

        playlist = spotify.get_playlist(title)
        if not playlist:
            logger.warning("Could not find playlist on Spotify")
            continue

        num_matched_songs = gpm.create_playlist(playlist)
        logger.info(f"Ceated playlist on GPM. Matched {num_matched_songs} of {len(playlist.songs)} songs")


if __name__ == '__main__':
    logger.info('Starting..')

    playlist_titles = sys.argv[1:]
    if playlist_titles:
        weekday = datetime.utcnow().date().weekday()
        if weekday == 0:
            logger.info("It's Monday! Copying..")
            main(playlist_titles)
        else:
            logger.info("It's not Monday! Quitting..")
    else:
        logger.warning("No playlists entered..")
