import json

with open('./withgender.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()

for member in members:
    tempMembers = dict()

    tempMembers['prefix'] = member['prefix']
    tempMembers['name'] = member['name']
    tempMembers['prefix'] = member['prefix']
    tempMembers['memberName'] = member['memberName']
    tempMembers['gender'] = member['gender']
    tempMembers['birthPlace'] = member['place_of_birth']
    tempMembers['maritalStatus'] = member['marital_status']
    tempMembers['sons'] = member['sons']
    tempMembers['daughters'] = member['daughters']
    tempMembers['email'] = list()
    tempMembers['phone'] = member['phone']
    tempMembers['profession'] = member['profession']
    tempMembers['education'] = member['education']
    tempMembers['terms'] = member['terms']
    tempMembers['expertise'] = list()

    newMembers.append(tempMembers)

with open('withkeycleaning.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
    
