import os

from gmusicapi import Mobileclient

EMAIL_ADDRESS = os.environ.get('GPM_EMAIL_ADDRESS')
APP_PASSWORD = os.environ.get('GPM_APP_PASSWORD')


class GPM(object):
    pass