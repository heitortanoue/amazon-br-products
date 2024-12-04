import pandas as pd
import pymongo
from bson import json_util
from dotenv import load_dotenv
import os

load_dotenv()

mongo_connection_string = os.getenv('MONGODB_CONNECTION_STRING')

client = pymongo.MongoClient(mongo_connection_string, timeoutMS=10*60*1000)
db = client['olistDB']

def dump_collection(collection, output_dir):
    try:
        data = list(collection.find())
        json_data = json_util.dumps(data, indent=4)
        output_file = os.path.join(output_dir, f"{collection.name}.json")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_data)
            print(f"Dumped collection '{collection.name}' to '{output_file}'")
    except Exception as e:
        print(f"Error dumping collection '{collection.name}': {e}")

def dump_database(db, output_dir='db_dump'):
    try:
        os.makedirs(output_dir, exist_ok=True)

        collections = db.list_collection_names()
        print(f"Found collections: {collections}")

        for collection_name in collections:
            collection = db[collection_name]
            dump_collection(collection, output_dir)

        print(f"Database dump completed. All collections are saved in '{output_dir}' directory.")
    except Exception as e:
        print(f"Error dumping database: {e}")

if __name__ == "__main__":
    output_directory = 'db_dump'
    dump_database(db, output_dir=output_directory)
