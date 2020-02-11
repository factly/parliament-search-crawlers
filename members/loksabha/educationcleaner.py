import json

with open('./withchild.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

phd =['Ph.D.','Ph. D', 'Doctorate']
ug = ['Engg','Bachelor of Engineering','B. A.','B.A','B.Com','B.Sc','L.L.B','B.E','B.B.M',
        'B.B.A','M.B.B.S','B.M.S.','C.A', 'B. Com','B. Sc','Undergraduate','Law','B. Tech.',
        'Universit','B.Tech.','B. Tech','Graduat']
pg = ['LL.M','M.A','M.Sc','M.Com','M.B.A','M.D','M.D.M','M.E','M.L','L.L.M','Graduate','Post Graduate','M. Com','Master','Masters']
inter =['Inter','Intermediate','Higher Secondary','PUC', 'Diploma']
school = ['High School', 'S.S.C', 'School','school']
undermatric = ['Under Matriculate','Under-Matric','Under Matric']
matric=['Matric','Matriculation']
    
newMembers = list()

for member in members: 
    if(member['__origin'] == "former"):
        edu = member['education'] 
        if any(x in edu for x in phd):
            member['education'] = 1
        elif any(x in edu for x in pg):
            member['education'] = 2
        elif any(x in edu for x in ug):
            member['education'] = 3
        elif any(x in edu for x in inter):
            member['education'] = 4
        elif any(x in edu for x in school):
            member['education'] = 5
        elif any(x in edu for x in matric):
            member['education'] = 5
        elif any(x in edu for x in undermatric):
            member['education'] = 6
        else:
            member['education'] = 7
    newMembers.append(member)

with open('witheducation.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)