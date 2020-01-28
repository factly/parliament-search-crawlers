import pymongo
import json

with open('./members/rajyasabha/cleanname.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./members/rajyasabha/m4.json', 'r', encoding='utf-8') as f:
    new_members = json.load(f)
    
config = json.load(open("./../config.cfg"))
        
client = pymongo.MongoClient(config['mongodb_uri'])
db = client[config['database']]

rsmembers = list(db.rs_members.find({}))

final = list()

for each in members:
    flist = list(filter(lambda member: member['name'] == " ".join(each['name'].split()) and member['prefix'] == each['prefix'], rsmembers))
    if(len(flist) == 1):
        new = flist[0]
        new['RSID'] = int(each['RSID'])
        del new['_id']
        final.append(new)
    else:
        print(each['name'])

print("########")

for each in new_members:
    flist = list(filter(lambda member: member['name'] == " ".join(each['name'].split()) and member['prefix'] == each['prefix'], rsmembers))
    if(len(flist) == 1):
        each['terms'] = flist[0]['terms']
        each['RSID'] = each['MID']
        final.append(each)
    else:
        print(each['name'])

print(len(final))

with open('withID2.json', 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=4)