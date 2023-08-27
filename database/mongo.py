import os
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URL"])
db = client[os.environ["MONGO_DB"]]