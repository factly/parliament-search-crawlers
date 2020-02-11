import dateutil.parser as dparser
import json
from datetime import datetime

with open('./final_2/withparty_2.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()

for member in members:
    if(member['__origin'] == "former"):
        if 'dob' in member:
            dob = member['dob']
            try:
                finalDOB = dparser.parse(dob,fuzzy=True)
                finalDOB = datetime.timestamp(finalDOB) * 1000        
            except:
                finalDOB = None
        else:
            finalDOB = None

        member['dob'] = finalDOB
    newMembers.append(member)


with open('./withdob.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
    