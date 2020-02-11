import json

with open('./withdob.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()

for member in members:
    if(member['__origin'] == "former"):
        newMarital = None

        if 'marital_status' in member:
            ms = member['marital_status']
            if "Unmarried" in ms:
                newMarital = 4
            elif "Married" in ms:
                newMarital = 1
            elif "MARRIED" in ms:
                newMarital = 1
            elif "Widower" in ms:
                newMarital = 5
        
        member['marital_status'] = newMarital
    newMembers.append(member)


with open('./withmarital.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
    