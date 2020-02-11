import json

with open('./withfinalconstituency_2.json', 'r', encoding='utf-8') as f:
    members = json.load(f)


with open('./party_dict.json', 'r', encoding='utf-8') as f:
    parties = json.load(f)

newMembers = list()

for member in members:
    newTerm = list()
    for term in member['terms']:
        term['party'] = parties[term['party'].strip()]

        newTerm.append(term)

    member['terms'] = newTerm

    newMembers.append(member)

with open('./withparty_2.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)