# utils/db_connection.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    mongo_connection_string = os.getenv('MONGODB_CONNECTION_STRING')
    if not mongo_connection_string:
        raise ValueError("MONGODB_CONNECTION_STRING is not set in the environment variables.")
    client = MongoClient(mongo_connection_string)
    db = client['olistDB']
    return db
