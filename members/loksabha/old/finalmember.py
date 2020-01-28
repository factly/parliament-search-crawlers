import json

with open('./withtermsclean.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()
for member in members:
    newMember = dict()
    newMember['MID'] = int(member['MID'])
    newMember['name'] = member['name']
    newMember['terms'] = member['terms']
    newMember['birthPlace'] = member['birth_place']
    newMember['prefix'] = member['prefix']
    newMember['fullName'] = member['fullName']
    
    if(member['dob']):
        newMember['dob'] = int(member['dob'])
    else:
        newMember['dob'] = None   

    if(member['marital_status']):
        newMember['maritalStatus'] = int(member['marital_status'])
    else:
        newMember['maritalStatus'] = None

    if(member['sons']):
        newMember['sons'] = int(member['sons'])
    else:
        newMember['sons'] = None

    if(member['daughters']):
        newMember['daughters'] = int(member['daughters'])
    else:
        newMember['daughters'] = None   

    if(member['education']):
        newMember['education'] = int(member['education'])
    else:
        newMember['education'] = None   

    if(member['gender']):
        newMember['gender'] = int(member['gender'])
    else:
        newMember['gender'] = None   
    

    if(member['__origin'] == "former"):
        newMember['email'] = list()
        newMember['phone'] = list()
    else:
        newMember['email'] = member['email']
        newMember['phone'] = member['phone']
    
    
    newMembers.append(newMember)

with open('./upload/ls_members.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
        