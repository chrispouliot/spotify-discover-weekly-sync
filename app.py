import logging

from musicclient import GPMClient, SpotifyClient


def main():
    spotify = SpotifyClient()
    gpm = GPMClient()
    disco_weekly = spotify.get_playlist("Discover Weekly")
    if not disco_weekly:
        logging.warning("Could not find playlist on Spotify")

    num_matched_songs = gpm.create_playlist(disco_weekly)
    logging.warning(f"Ceated playlist on GPM. Matched {num_matched_songs} of {len(disco_weekly.songs)} songs")


if __name__ == '__main__':
    logging.warning('Starting..')
    main()