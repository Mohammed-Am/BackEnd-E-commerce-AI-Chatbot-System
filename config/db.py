import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

def get_db():
    try:
        mongo = pymongo.MongoClient(os.environ.get("MONGO_URI"))
        db = mongo.get_database('bike_shop')
        print("MongoDB connected successfully!")
        return db
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None
