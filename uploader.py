import pymongo
import json

config = json.load(open("./config.cfg"))
        
client = pymongo.MongoClient(config['mongodb_uri'])
db = client[config['database']]

with open('./members/comman/all_members.json', 'r', encoding='utf-8') as f:
    list = json.load(f)

db.all_members.insert_many(list)
