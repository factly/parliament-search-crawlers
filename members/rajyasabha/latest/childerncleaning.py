import json

with open('./cleannamewithterms.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

newMembers = list()

for member in members:
    childern = member['children'].lower()
    if(childern != "-"):
        childList = childern.split(" ")
        if "son" in childList:
            sonPost = childList.index("son")
            if(sonPost >= 1):
                sonWord = childList[sonPost - 1]
                if(sonWord in units):
                    sonUnit = units.index(sonWord)
                    member['sons'] = sonUnit
                else:
                    print('son unit error', member['name'])
            else:
                print("son index zero", member['name'])
        elif "sons" in childList:
            sonPost = childList.index("sons")
            if(sonPost >= 1):
                sonWord = childList[sonPost - 1]
                if(sonWord in units):
                    sonUnit = units.index(sonWord)
                    member['sons'] = sonUnit
                else:
                    print('sons unit error', member['name'])
            else:
                print("sons index zero", member['name'])
        
        if "daughter" in childList:
            daughterPost = childList.index("daughter")
            if(daughterPost >= 1):
                daughterWord = childList[daughterPost - 1]
                if(daughterWord in units):
                    daughterUnit = units.index(daughterWord)
                    member['daughters'] = daughterUnit
                else:
                    print('daughter unit error', member['name'])
            else:
                print("daughter index zero", member['name'])
        elif "daughters" in childList:
            daughterPost = childList.index("daughters")
            if(daughterPost >= 1):
                daughterWord = childList[daughterPost - 1]
                if(daughterWord in units):
                    daughterUnit = units.index(daughterWord)
                    member['daughters'] = daughterUnit
                else:
                    print('daughter unit error', member['name'])
            else:
                print("daughter index zero", member['name'])

        if 'sons' not in member:
            member['sons'] = None
        
        if 'daughters' not in member:
            member['daughters'] = None

    else:
        member['sons'] = None
        member['daughters'] = None

    newMembers.append(member)

with open('withchild.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
