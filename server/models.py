from datetime import datetime
from bson.objectid import ObjectId

from pymongo import MongoClient

from .config import MONGO_URL

_client = MongoClient(MONGO_URL)
_db = _client['spotify-sync']
_sessions = _db.sessions


class Session:

    @staticmethod
    def create(access_token, refresh_token, expiry_date):
        obj_id = _sessions.insert_one({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expiry_date': expiry_date,
            'created_date': datetime.utcnow(),
        }).inserted_id
        return str(obj_id)

    @staticmethod
    def get(str_id):
        return _sessions.find_one({'_id': ObjectId(str_id)})
