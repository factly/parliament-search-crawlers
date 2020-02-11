import json

with open('./all_members_terms.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newSession = dict()
for session in members:
    newMembers = list()
    for member in members[session]:
        nameList = member['name'].split(",")

        if(len(nameList) == 2):
            fullname = nameList[1].strip() + " " + nameList[0].strip()
        elif(len(nameList) == 1):
            fullname = nameList[0].strip()
        else:
            print(nameList)
        if(fullname):
            fullname = fullname.strip()

            member['name'] = fullname

            newMembers.append(member)

    newSession[session] = newMembers

with open('./termswithcleanname.json', 'w', encoding='utf-8') as f:
    json.dump(newSession, f, ensure_ascii=False, indent=4)

    