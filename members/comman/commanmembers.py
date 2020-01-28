import pymongo
import json
import csv

config = json.load(open("./../config.cfg"))
        
client = pymongo.MongoClient(config['mongodb_uri'])
db = client[config['database']]

with open('./geographies/final_geo.json', 'r', encoding='utf-8') as f:
    geos = json.load(f)

geoDict = dict()

for geo in geos:
    geoDict[int(geo['GID'])] = geo['name']

geoDict[None] = "Ind."

abc = list(db.ls_members.aggregate([
    {
        '$lookup': {
            'from': 'rs_members',
            'localField': 'name',
            'foreignField': 'name',
            'as': 'matching'
        }
    },
    {
        '$match': {
            'matching': { 
                '$not': {
                    '$size': 0
                }
            }
        }
    }
]))

comman = list()
for each in abc:
    tempDict = list()
    tempDict.append(each['MID'])
    tempDict.append(each['matching'][0]['MID'])
    tempDict.append(each['name'])
    tempDict.append(", ".join(list(map(lambda term: geoDict[term['constituency']], each['terms']))))
    tempDict.append(", ".join(list(map(lambda term: geoDict[term['geography']], each['matching'][0]['terms']))))
    
   
    comman.append(tempDict)

    if len(each['matching']) != 1:
        print(each)
        

with open('members/comman/ls_rs_comman.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(comman)