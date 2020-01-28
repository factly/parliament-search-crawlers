import json

with open('./all_members.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()
for member in members:
    nameList = member['name'].split(",")

    fullname = nameList[1].strip() + " " + nameList[0].strip()

    fullname = fullname.strip()

    member['name'] = fullname

    newMembers.append(member)

with open('./withcleanname.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)

    