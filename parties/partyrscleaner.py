import json

with open('./rs_members.json', 'r', encoding='utf-8') as f:
    rs_members = json.load(f)

with open('./partydontknow.json', 'r', encoding='utf-8') as f:
    rs_changer = json.load(f)


newMembers = list()

for rs_member in rs_members:
    newTerms = list()
    for term in rs_member['terms']:
        term['party'] = rs_changer[str(term['party'])]

        newTerms.append(term)
    
    rs_member['terms'] = newTerms

    newMembers.append(rs_member)

with open('rs_final_members.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)