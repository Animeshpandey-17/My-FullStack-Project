# myproject/myapp/mongo_connection.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_mongo_client():
    # Retrieve credentials from environment variables
    username = os.getenv('MONGO_USERNAME')  # 'ani'
    password = os.getenv('MONGO_PASSWORD')  # 'ani17'
    db_name = os.getenv('MONGO_DB_NAME')     # 'ani'
    host = 'cluster0.wje1q.mongodb.net'

    # Construct the connection string
    connection_string = f"mongodb+srv://ani:ani17@cluster0.wje1q.mongodb.net/ani?retryWrites=true&w=majority&appName=Cluster0"
    
    # Create a MongoClient instance
    client = MongoClient(connection_string)
    return client

def get_blacklist_collection():
    client = get_mongo_client()
    db = client['ani']
    return db['blacklisted_tokens']
