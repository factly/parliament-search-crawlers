import json

with open('./withprof.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

newMembers = list()

for member in members:
    mobileRow = member['permanent_phone']
    mobileList = list()
    if(mobileRow):
        mobile = mobileRow.replace("{", "")
        mobile = mobile.replace("}", "")
        mobile = mobile.replace("-", "")
        mobile = mobile.replace("(O)", "")
        mobile = mobile.replace("(R)", "")
        mobile = mobile.replace("(F)", "FAX")
        mobile = mobile.replace("(", "")
        mobile = mobile.replace(")", "")

        mobile = mobile.replace("Mobile", "")
        mobile = mobile.replace("Mob", "")
        mobile = mobile.replace("M", "")
        mobile = mobile.replace("Tel", "")
        mobile = mobile.replace(":", "")
        mobile = mobile.replace(";", "")
        mobile = mobile.replace(".", "")
        mobile = mobile.replace(" ", "")
        
        

        for each in mobile.split(","):
            if each:
                if each.isnumeric():
                    mobileList.append(each)
                else:
                    print("NEW")
                    print(mobileRow)
                    print(each)
    
    member['phone'] = mobileList
    newMembers.append(member)


with open('withphone.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)