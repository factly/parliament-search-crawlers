import json

with open('./data/constituency.json', 'r', encoding='utf-8') as f:
    constituencies = json.load(f)

with open('./data/states.json', 'r', encoding='utf-8') as f:
    states = json.load(f)

newConstituency = list()

for constituency in constituencies:
    constituency['parent'] = states[constituency['state']]
    constituency['which'] = 'constituency'
    newConstituency.append(constituency)


with open('./constituency_all.json', 'w', encoding='utf-8') as f:
    json.dump(newConstituency, f, ensure_ascii=False, indent=4)