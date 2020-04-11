import json

with open('./rs_latest.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()

for each in members:
    each['memberName'] = each['name']
    
    name = each['name']
    if 'Shri' in name:
        newName = name.split('Shri', 1)
        prefix = 'Shri'
    elif 'Smt.' in name:
        newName = name.split('Smt.', 1)
        prefix = 'Smt.'
    elif 'Dr.' in name:
        newName = name.split('Dr.', 1)
        prefix = 'Dr.'
    elif 'Prof.' in name:
        newName = name.split('Prof.', 1)
        prefix = 'Prof.'
    elif 'Ms.' in name:
        newName = name.split('Ms.', 1)
        prefix = 'Ms.'
    elif 'Miss' in name:
        newName = name.split('Miss', 1)
        prefix = 'Miss'
    elif 'Kumari' in name:
        newName = name.split('Kumari', 1)
        prefix = 'Kumari'
    elif 'Sardar' in name:
        newName = name.split('Sardar', 1)
        prefix = 'Sardar'
    elif 'Chaudhary' in name:
        newName = name.split('Chaudhary', 1)
        prefix = 'Chaudhary'
    elif 'Ch.' in name:
        newName = name.split('Ch.', 1)
        prefix = 'Chaudhary'
    elif 'Mahant' in name:
        newName = name.split('Mahant', 1)
        prefix = 'Mahant'
    elif 'Mir' in name:
        newName = name.split('Mir', 1)
        prefix = 'Mir'
    
    
    else:
        print(name)
        newName = name
        prefix = None

    if(prefix == None):
        each['name'] = name
    else:
        each['name'] = (newName[-1] + " " + newName[0]).strip()
    
    each['prefix'] = prefix
    each['questions'] = list()
    newMembers.append(each)
    
with open('cleanname.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
