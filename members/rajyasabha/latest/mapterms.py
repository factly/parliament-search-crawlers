import json

with open('./withkeycleaning.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./states.json', 'r', encoding='utf-8') as f:
    states = dict(json.load(f))

with open('./parties.json', 'r', encoding='utf-8') as f:
    parties = dict(json.load(f))

newMembers = list()

for member in members:
    terms = list()
    for term in member['terms']:
        temp = dict()
        temp['house'] = 2
        temp['session'] = None
        temp['geography'] = states[term['state']]
        temp['party'] = parties[term['party']]
        temp['from'] = term['from']
        temp['to'] = term['to']

        terms.append(temp)

    member['terms'] = terms

    newMembers.append(member)

with open('withalldetails.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)