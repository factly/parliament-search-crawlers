import json

with open('./members/loksabha/old/final/ls_all_members.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()
for each in members:
    each['LSID'] = each['MID']
    newMembers.append(each)
    

with open('withID2.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)