from pymongo import MongoClient
client = MongoClient("localhost", 27017)
db = client.mydb
users = db.users
blogs = db.blogs
categories = db.categories