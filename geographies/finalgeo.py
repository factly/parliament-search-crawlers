import json

with open('./final_2/constituency_all.json', 'r', encoding='utf-8') as f:
    geos = json.load(f)

newGeos = list()

categoryList = ["SC", "ST", "GEN"]

for geo in geos:
    tempGeo = dict()
    tempGeo['GID'] = int(geo['GID'])
    tempGeo['name'] = geo['name']
    tempGeo['type'] = geo['which']
    tempGeo['parent'] = geo['parent']
    tempGeo['category'] = categoryList[int(geo['type'] - 1)]

    newGeos.append(tempGeo)
    
with open('./upload/final_geo.json', 'w', encoding='utf-8') as f:
    json.dump(newGeos, f, ensure_ascii=False, indent=4)
        