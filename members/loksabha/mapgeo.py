import json

with open('./withmeta_2.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./constituency.json', 'r', encoding='utf-8') as f:
    constituency = json.load(f)

with open('./notoddgeo.json', 'r', encoding='utf-8') as f:
    oddgeo = json.load(f)


newMembers = list()

for member in members:
    newTerms = list()
    for term in member['terms']:
        if term['constituency'] != "" and len(term['constituency'].replace("(SC)", "").replace("(ST)", "").split("(")) == 2:
            tempGeo = dict()
            geo = term['constituency'].strip()
            tempGeo['full'] = geo
            SCfind = geo.find("(SC)")
            STfind = geo.find("(ST)")

            if(SCfind >= 0):
                tempGeo['type'] = 1
            elif(STfind >= 0):
                tempGeo['type'] = 2
            else:
                tempGeo['type'] = 3

            stateCleaning = geo.replace("(SC)", "").replace("(ST)", "").split("(")

            tempGeo['name'] = stateCleaning[0].strip()
            tempGeo['state'] = stateCleaning[1].replace(")", "").strip()


            
            secondSCfind = geo.find("-SC")
            secondSTfind = geo.find("-ST")

            if(secondSCfind >= 0):
                tempGeo['name'] = tempGeo['name'].split("-SC")[0].strip()
                tempGeo['type'] = 1
            elif(secondSTfind >= 0):
                tempGeo['name'] = tempGeo['name'].split("-ST")[0].strip()
                tempGeo['type'] = 2

            GIDlist = list(filter(lambda geo: geo['name'] == tempGeo['name'] and geo['type'] == tempGeo['type'] and geo['state'] == tempGeo['state'], constituency))
            
            if(len(GIDlist) == 1):
                term['constituency'] = int(GIDlist[0]['GID'])
            else:
                print(term['constituency'])
        elif term['constituency'].strip() == "":
            term['constituency'] = None
        elif term['constituency'].strip() in oddgeo:
            term['constituency'] = oddgeo[term['constituency'].strip()]
        else:
            print(term['constituency'])
        
        newTerms.append(term)

    member['terms'] = newTerms

    newMembers.append(member)  

with open('./withfinalconstituency_2.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)