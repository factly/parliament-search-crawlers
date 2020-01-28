import xlrd 
import json
import datetime
n = 1
wb = xlrd.open_workbook('rsold.xlsx') 
sheet = wb.sheet_by_index(n -1) 
print(sheet)
result = list()

# For row 0 and column 0 
for i in range(1, 1347, n):
    print(sheet.cell_value(i, 1))
    temp = dict()
 
    temp['name'] = sheet.cell_value(i, 1)
    temp['term'] = list()

    for j in range(0, n):
        state = sheet.cell_value(i + j, 2)
        party = sheet.cell_value(i + j, 3)
        termFrom = sheet.cell_value(i + j, 4)
        termTo = sheet.cell_value(i + j, 5)
        termReason = sheet.cell_value(i + j, 6)

        if termReason != "Retirement":
            termToFinal = termReason
        else:
            termToFinal = termTo
        termFromFinal = xlrd.xldate_as_tuple(termFrom, 0)
        termToFinal2 = xlrd.xldate_as_tuple(termToFinal, 0)

        term = dict()
        term['state'] = state
        term['party'] = party
        term['from'] = str(termFromFinal[0]) + "-" + str(termFromFinal[1]) + "-" + str(termFromFinal[2])
        term['to'] = str(termToFinal2[0]) + "-" + str(termToFinal2[1]) + "-" + str(termToFinal2[2])

        temp['term'].append(term)
   

    result.append(temp)

with open('dataold1.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

#terms 2 Manohar Kant only 1 avalibale