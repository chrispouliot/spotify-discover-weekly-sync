import sys

from datetime import datetime

from config import logger
from musicclient import GPMClient, SpotifyClient


def main(playlist_titles):
    if not playlist_titles:
        logger.warning("No playlists entered, exiting..")
        return

    spotify = SpotifyClient()
    gpm = GPMClient()

    for title in playlist_titles:
        logger.info(f"Attempting to copy playlist '{title}'..")

        playlist = spotify.get_playlist(title)
        if not playlist:
            logger.warning("Could not find playlist on Spotify")
            continue

        num_matched_songs = gpm.create_playlist(playlist)
        logger.info(f"Ceated playlist on GPM. Matched {num_matched_songs}/{len(playlist.songs)} songs")


if __name__ == '__main__':
    logger.info('Starting..')

    weekday = datetime.utcnow().date().weekday()
    if weekday == 0:
        logger.info("It's Monday! Copying..")
        main(sys.argv[1:])  # Pass playlist title cli args
    else:
        logger.info("It's not Monday! Quitting..")
