import json
import pymongo
import xlrd

with open('./cleanname.json', 'r', encoding='utf-8') as f:
    members = json.load(f)
    

wb = xlrd.open_workbook('rscurrent.xlsx') 
sheet = wb.sheet_by_index(0)

def searchNameInExcel(name):
    for i in range(0, 242):
        if(name == sheet.cell_value(i, 3)):
            return i
            break

    return None

def strCleaner(name):
    return name.replace("'", "").strip()
    
config = json.load(open("./../config.cfg"))
        
client = pymongo.MongoClient(config['mongodb_uri'])
db = client[config['database']]

newMembers = list()

for rslocal in members:
    localname = rslocal['name']
    
    rsdb = db.rscleanedMembers.find_one({'name': localname})
    number = searchNameInExcel(localname)

    if(rsdb):
        rsdb['terms'] = rslocal['terms']
        rsdb['_id'] = None
        newMembers.append(rsdb)

    elif(number):
        oldProf = sheet.cell_value(number, 13)
        if(oldProf):
            prof = sheet.cell_value(number, 13)[1:-1].split(",") 

            newProf = map(strCleaner, prof)
        else: 
            newProf = list()

        olddob = sheet.cell_value(number, 9)
        if(olddob):
            xldob = xlrd.xldate_as_tuple(olddob, 0)
            dob = str(xldob[0]) + "-" + str(xldob[1]) + "-" + str(xldob[2])
        else:
            dob = None
        rslocal['sons'] = int(sheet.cell_value(number, 6))
        rslocal['daughters'] = int(sheet.cell_value(number, 7))
        rslocal['maritalStatus'] = int(sheet.cell_value(number, 11))
        rslocal['education'] = int(sheet.cell_value(number, 12))
        rslocal['phone'] = list()
        rslocal['dob'] = dob
        rslocal['birthPlace'] = sheet.cell_value(number, 10)
        rslocal['email'] = list()
        rslocal['email'].append(sheet.cell_value(number, 8))
        rslocal['profession'] = list(newProf)
        rslocal['expertise'] = list()
        
        
        newMembers.append(rslocal)
    else:
        print(localname)
 
with open('allmix.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)
