from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import getenv


# Create a new client and connect to the server
client = MongoClient(getenv("MONGO_DB_URI"), server_api=ServerApi('1'))

db = client.mydb
users = db.users
blogs = db.blogs
categories = db.categories
