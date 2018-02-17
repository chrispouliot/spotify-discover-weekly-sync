import logging

from musicclient import GPMClient, SpotifyClient


def main():
    spotify = SpotifyClient()
    disco_weekly = spotify.get_playlist("Discover Weekly")
    logging.warning("Got playlist")
    logging.warning("Total tracks: {}".format(len(disco_weekly.songs)))


if __name__ == '__main__':
    logging.warning('Starting..')
    main()