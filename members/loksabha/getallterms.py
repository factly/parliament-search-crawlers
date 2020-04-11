import xlrd 
import json

final = dict()

wb = xlrd.open_workbook('./members/loksabha/ls_members.xlsx') 

sheet = wb.sheet_by_index(0)


for i in range(1, 18):
    sheet = wb.sheet_by_index(i - 1)
    temp = list()
    for each in range(1, sheet.nrows):
        temp.append({
            'name': sheet.cell_value(each, 1),
            'party': sheet.cell_value(each, 2),
            'constituency': sheet.cell_value(each, 3)
        })

    final[i] = temp

with open('./members/loksabha/all_ls_members_2.json', 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=4)

