import os
import pymongo
from dotenv import load_dotenv
import certifi
import ssl

load_dotenv()

def get_db():
    try:
        ca = certifi.where()
        mongo = pymongo.MongoClient(
            os.environ.get("MONGO_URI"),
            tls=True,
            tlsCAFile=ca,
            tlsAllowInvalidCertificates=False,
            tlsAllowInvalidHostnames=False
        )
        db = mongo.get_database('bike_shop')
        print("MongoDB connected successfully!")
        return db
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None
