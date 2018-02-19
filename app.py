import logging

from datetime import datetime

from musicclient import GPMClient, SpotifyClient


def main():
    spotify = SpotifyClient()
    gpm = GPMClient()
    disco_weekly = spotify.get_playlist("Discover Weekly")
    if not disco_weekly:
        logging.warning("Could not find playlist on Spotify")
        return

    num_matched_songs = gpm.create_playlist(disco_weekly)
    logging.warning(f"Ceated playlist on GPM. Matched {num_matched_songs} of {len(disco_weekly.songs)} songs")


if __name__ == '__main__':
    logging.warning('Starting..')
    # Temporary date check for use in my weekly cron of this script.
    weekday = datetime.utcnow().date().weekday()
    if weekday == 0:
        logging.warning("It's Monday! Copying playlist..")
        main()
    else:
        logging.warning("It's not Monday! Quitting..")
