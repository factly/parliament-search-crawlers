import json

with open('./withprof.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./withmarital.json', 'r', encoding='utf-8') as f:
    preMembers = json.load(f)

preMembersDict = dict()
for pre in preMembers:
    preMembersDict[pre['MID']] = pre['name']


prefixSet = set()
newMembers = list()
for member in members:
    nameList = member['name'].split(" ", 1)
    member['prefix'] = nameList[0]
    member['name'] = nameList[1]
    member['fullName'] = preMembersDict[member['MID']]
    
    prefixSet.add(nameList[0])

    newMembers.append(member)

print(prefixSet)

with open('withprefix.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
