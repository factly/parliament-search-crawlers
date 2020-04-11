import json

with open('./withphone.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()

prefixGenderMatching = {
    'Shri': 2,
    'Smt.': 1,
    'Dr.': 0,
    'Prof.': 0,
    'Ms.': 1,
    'Miss': 1,
    'Kumari': 1,
    'Sardar': 2,
    'Chaudhary': 2,
    'Ch.': 2,
    'Mahant': 2,
    'Mir': 2
}

for member in members:
    member['gender'] = prefixGenderMatching[member['prefix']]
    
    newMembers.append(member)

    
with open('withgender.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
