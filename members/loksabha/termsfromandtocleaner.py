import json
import datetime
import time

with open('./withprefix.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()
for member in members:
    newTerms = list()
    for term in member['terms']:
        term['from'] = int(time.mktime(datetime.datetime.strptime(term['from'], "%d/%m/%Y").timetuple()) * 1000)
        if term['to'] != "":
            term['to'] = int(time.mktime(datetime.datetime.strptime(term['to'], "%d/%m/%Y").timetuple()) * 1000)  
        
        newTerms.append(term)

    member['terms'] = newTerms

    newMembers.append(member)


with open('withtermsclean.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
        