import json

with open('./cleanname.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

termsDict = dict()

for term in terms:
    termsDict[term['name']] = term

newMembers = list()

for member in members:
    if member['name'] in termsDict:
        member['terms'] = termsDict[member['name']]['terms']
    else:
        print(member['name'])

    newMembers.append(member)
    
with open('withterms.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
