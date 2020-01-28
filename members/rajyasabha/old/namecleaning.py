import json

with open('./members/rajyasabha/witha.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()

for each in members:
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
    elif 'Sardar' in name:
        newName = name.split('Sardar', 1)
        prefix = 'Sardar'
    elif 'Maulana' in name:
        newName = name.split('Maulana', 1)
        prefix = 'Maulana'
    elif 'Chaudhary' in name:
        newName = name.split('Chaudhary', 1)
        prefix = 'Chaudhary'
    elif 'Begum' in name:
        newName = name.split('Begum', 1)
        prefix = 'Begum'
    elif 'Kumari' in name:
        newName = name.split('Kumari', 1)
        prefix = 'Kumari'
    elif 'Pandit' in name:
        newName = name.split('Pandit', 1)
        prefix = 'Pandit'
    elif 'Chowdhary' in name:
        newName = name.split('Chowdhary', 1)
        prefix = 'Chowdhary'

    else:
        print(name)
        newName = name
        prefix = None

    if(prefix == None):
        each['name'] = name
    else:
        each['name'] = (newName[-1] + " " + newName[0]).strip()
    
    each['prefix'] = prefix

    newMembers.append(each)
    
with open('cleanname.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
