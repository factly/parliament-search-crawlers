import json

with open('./geographies/constituency.json', 'r', encoding='utf-8') as f:
    constituencies = json.load(f)

geoDict = dict()

count = 0
for constituency in constituencies:
    key = constituency['name'] + constituency['state']
    if key not in geoDict:
        geoDict[key] = constituency
    else:
        count += 1

print(count)