import json
import datetime
import time
with open('./withchild.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()
for member in members:
    dob = member["dob"]
    if dob != "-":
        newDob = time.mktime(datetime.datetime.strptime(dob, "%d %B %Y").timetuple())
        member['dob'] = newDob
        member['dobFull'] = dob
    else:
        member['dob'] = None
        member['dobFull'] = None

    if "Unmarried" in member['marital_status']:
        member['marital_status'] = 4
    elif "Married" in member['marital_status']:
        member['marital_status'] = 1
    elif "Divorced" in member['marital_status']:
        member['marital_status'] = 3
    else:
        member['marital_status'] = 6
    
    newMembers.append(member)

with open('withdobstamp.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)

    