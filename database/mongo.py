import yaml
from pymongo import MongoClient

with open('secrets.yml', 'r') as file:
    config = yaml.safe_load(file)

client = MongoClient(config["MongoDB"]["ATLAS_URI"])
db = client["ReminderBot"]