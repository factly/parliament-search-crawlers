import pymongo
import json

config = json.load(open("./config.cfg"))
        
client = pymongo.MongoClient(config['mongodb_uri'])
db = client[config['database']]

with open('./q17_with_ID.json', 'r', encoding='utf-8') as f:
    list = json.load(f)

db.all_questions.insert_many(list)
