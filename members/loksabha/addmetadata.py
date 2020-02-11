import json

with open('./withterms.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./ls_former.json', 'r', encoding='utf-8') as f:
    ls_former = json.load(f)

with open('./ls_current.json', 'r', encoding='utf-8') as f:
    ls_current = json.load(f)

newMembers = list()
for member in members:
    MID = member['MID']

    currentList = list(filter(lambda person: person['MID'] == int(MID), ls_current))

    if(len(currentList) == 1):
        currentMember = currentList[0]
        member['gender'] = currentMember['gender']
        member['dob'] = currentMember['dob']
        member['birth_place'] = currentMember['birthPlace']
        member['marital_status'] = currentMember['maritalStatus']
        member['sons'] = currentMember['sons']
        member['daughters'] = currentMember['daughters']
        member['education'] = currentMember['education']
        member['profession'] = currentMember['profession']
        member['email'] = currentMember['email']
        member['phone'] = currentMember['phone']
        member['__origin'] = "current"
    else:
        formerList = list(filter(lambda person: person['_id'] == MID, ls_former))
        
        if(len(formerList) == 1):
            formerMember = formerList[0]
            member['gender'] = formerMember['gender']
            member['dob'] = formerMember['dob']
            member['birth_place'] = formerMember['birth_place']
            member['marital_status'] = formerMember['marital_status']
            member['sons'] = formerMember['sons']
            member['daughters'] = formerMember['daughters']
            member['education'] = formerMember['education']
            member['profession'] = formerMember['profession']
            member['__origin'] = "former"
        
        else:
            print(MID)
    
    newMembers.append(member)

allMembers = sorted(newMembers, key = lambda i: int(i['MID']))

with open('./withmeta_2.json', 'w', encoding='utf-8') as f:
    json.dump(allMembers, f, ensure_ascii=False, indent=4)
