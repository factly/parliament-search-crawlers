import json

with open('./geographies/india_pc_2019_simplified.json', 'r', encoding='utf-8') as f:
    cordinates = json.load(f)

with open('./geographies/states.json', 'r', encoding='utf-8') as f:
    states = json.load(f)

with open('./geographies/constituency.json', 'r', encoding='utf-8') as f:
    constituencies = json.load(f)

typeMapper = ['SC', 'ST', 'GEN']

constituenciesDict = dict()
for each in constituencies:
    constituenciesDict[each['name'] +"#"+each['state']+"#"+typeMapper[each['type'] - 1]] = each

newMap = list()

for each in cordinates['features']:
    if each['properties']['pc_name'] + "#" + each['properties']['st_name'] + "#" + each['properties']['pc_category'] in constituenciesDict:
        
        matched = constituenciesDict[each['properties']['pc_name'] + "#" + each['properties']['st_name'] + "#" + each['properties']['pc_category']]

        newProp = dict()

        newProp['GID'] = matched['GID']
        newProp['name'] = matched['name']
        newProp['state'] = matched['state']
        newProp['category'] = typeMapper[matched['type'] - 1]

        each['properties'] = newProp

        newMap.append(each)

with open('./geographies/new_map.json', 'w', encoding='utf-8') as f:
    json.dump(newMap, f, ensure_ascii=False, indent=4)