import json
import datetime
import time

with open('./withMIDnew.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()
for member in members:
    newTerms = list()
    for term in member['terms']:
        term['from'] = int(time.mktime(datetime.datetime.strptime(term['from'], "%Y-%m-%d").timetuple()) * 1000)
        if term['to'] != "":
            term['to'] = int(time.mktime(datetime.datetime.strptime(term['to'], "%Y-%m-%d").timetuple()) * 1000)  
        
        newTerms.append(term)

    member['terms'] = newTerms

    newMembers.append(member)


with open('withtermsclean.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
        