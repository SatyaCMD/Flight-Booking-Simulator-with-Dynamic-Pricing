import os
from pymongo import MongoClient
from django.conf import settings

class MongoDB:
    _client = None
    _db = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/flight_simulator')
            cls._client = MongoClient(mongo_uri)
        return cls._client

    @classmethod
    def get_db(cls):
        if cls._db is None:
            client = cls.get_client()
            # Parse db name from URI or use default
            db_name = client.get_default_database().name
            cls._db = client[db_name]
        return cls._db

def get_flights_collection():
    return MongoDB.get_db()['flights']

def get_airports_collection():
    return MongoDB.get_db()['airports']

def get_airlines_collection():
    return MongoDB.get_db()['airlines']

def get_users_collection():
    return MongoDB.get_db()['users']

def get_bookings_collection():
    return MongoDB.get_db()['bookings']
