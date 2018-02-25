import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_USER_ID = os.environ.get("SPOTIFY_USER_ID")
GPM_EMAIL_ADDRESS = os.environ.get('GPM_EMAIL_ADDRESS')
GPM_APP_PASSWORD = os.environ.get('GPM_APP_PASSWORD')
