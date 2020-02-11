import json
import xlrd 

wb = xlrd.open_workbook('genderdontknow.xlsx') 
sheet = wb.sheet_by_index(0)

with open('./upload/ls_members.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

genderDict = {
    "Male": 2,
    "Female": 1
}


def searchNameInExcel(MID):
    for i in range(0, 355):
        if(MID == sheet.cell_value(i, 0)):
            return genderDict[sheet.cell_value(i, 2)]
            break
newMembers = list()
for member in members:
    if(member['gender'] == None):
        genderNumber = searchNameInExcel(member['MID'])
        print(genderNumber)
        member['gender'] = genderNumber

    newMembers.append(member)


with open('./upload/ls_final_gender.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)

