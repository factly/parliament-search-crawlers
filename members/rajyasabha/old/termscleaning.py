import json

with open('./old/withmetacsv.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./states.json', 'r', encoding='utf-8') as f:
    states = dict(json.load(f))

with open('./parties.json', 'r', encoding='utf-8') as f:
    parties = dict(json.load(f))

newMembers = list()

for member in members:
    member['memberName'] = member['prefix'] + " " + member['name']
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


totalNewMember = list()
count = 9041

for member in members:
    member['MID'] = count
    count += 1
    totalNewMember.append(member)

with open('termsclean.json', 'w', encoding='utf-8') as f:
    json.dump(totalNewMember, f, ensure_ascii=False, indent=4)