import json

with open('./withmarital.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()
sonSet = set()
duaSet = set()
for member in members:
    if(member['__origin'] == "former"):

        if 'sons' in member:
            son = str(member['sons']).strip()
            if(son == 'Not Available'):
                newSons = None
            elif(son.isnumeric()):
                newSons = int(son)
            else:
                newSons = None
        else:
            newSons = None
        

        if 'daughters' in member:
            daughter = str(member['daughters']).strip()
            if(daughter == 'Not Available'):
                newDaughters = None
            elif(daughter.isnumeric()):
                newDaughters = int(daughter)
            else:
                newDaughters = None
        else:
            newDaughters = None

        sonSet.add(newSons)
        duaSet.add(newDaughters)
        member['sons'] = int(newSons)
        member['daughters'] = int(newDaughters)
    newMembers.append(member)



with open('./withchild.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)