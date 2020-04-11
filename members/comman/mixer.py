import json
import csv
with open('./members/loksabha/old/final/withID2.json', 'r', encoding='utf-8') as f:
    ls_members = json.load(f)

with open('./members/rajyasabha/withID2.json', 'r', encoding='utf-8') as f:
    rs_members = json.load(f)

commanMembers = list()

ls_ids = list()
rs_ids = list()

with open('./members/comman/final_comman.csv') as csv_file:
    comman = csv.reader(csv_file, delimiter=',')
    for each in comman:
        if(each[5] == 'Yes'):
            LS = list(filter(lambda member: int(member['MID']) == int(each[0]), ls_members))
            RS = list(filter(lambda member: int(member['MID']) == int(each[1]), rs_members))
            
            ls_m = LS[0]
            if(len(RS) != 1):
                print(each)

            ls_ids.append(int(LS[0]['MID']))
            rs_ids.append(int(RS[0]['MID']))

            ls_m['terms'] = LS[0]['terms'] + RS[0]['terms']
            ls_m['RSID'] = RS[0]['RSID']
            commanMembers.append(ls_m)

with open('./members/comman/mixed.json', 'w', encoding='utf-8') as f:
    json.dump(commanMembers, f, ensure_ascii=False, indent=4)

otherMembers = list()
ls_miss = 0
rs_miss = 0
rs_temp = list()
for each_ls in ls_members:
    if int(each_ls['MID']) not in ls_ids:
        otherMembers.append(each_ls)
    else:
        ls_miss += 1

for each_rs in rs_members:
    if int(each_rs['MID']) not in rs_ids:
        otherMembers.append(each_rs)
    else:
        rs_temp.append(each_rs['MID'])
        rs_miss += 1
print(rs_miss)
print(len(rs_ids))

print(ls_miss)
print(len(ls_ids))

with open('./members/comman/onlyone.json', 'w', encoding='utf-8') as f:
    json.dump(otherMembers, f, ensure_ascii=False, indent=4)
