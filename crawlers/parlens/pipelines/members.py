from scrapy.exceptions import DropItem

class NameCleaner(object):
    def process_item(self, item, spider):

        nameList = " ".join(item['name'].split()).split(",", 1)
        if(len(nameList) == 2):
            fullname = nameList[1].strip() + " " + nameList[0].strip()
        else:
            fullname = nameList[0].strip()

        fullNameList = fullname.split(" ", 1)
        item['prefix'] = fullNameList[0].strip()
        item['name'] = fullNameList[1].strip()
        item['memberName'] = fullname

        return item

class EducationCleaner(object):
    def process_item(self, item, spider):
        if 'education' in item and item['education'] != None:
            phd =['Ph.D.','Ph. D', 'Doctorate']
            ug = ['Engg','Bachelor of Engineering','B. A.','B.A','B.Com','B.Sc','L.L.B','B.E','B.B.M',
                    'B.B.A','M.B.B.S','B.M.S.','C.A', 'B. Com','B. Sc','Undergraduate','Law','B. Tech.',
                    'Universit','B.Tech.','B. Tech','Graduat']
            pg = ['LL.M','M.A','M.Sc','M.Com','M.B.A','M.D','M.D.M','M.E','M.L','L.L.M','Graduate','Post Graduate','M. Com','Master','Masters']
            inter =['Inter','Intermediate','Higher Secondary','PUC', 'Diploma']
            school = ['High School', 'S.S.C', 'School','school']
            undermatric = ['Under Matriculate','Under-Matric','Under Matric']
            matric=['Matric','Matriculation']

            edu = item['education']
            
            if any(x in edu for x in phd):
                eduNo = 1
            elif any(x in edu for x in pg):
                eduNo = 2
            elif any(x in edu for x in ug):
                eduNo = 3
            elif any(x in edu for x in inter):
                eduNo = 4
            elif any(x in edu for x in school):
                eduNo = 5
            elif any(x in edu for x in matric):
                eduNo = 5
            elif any(x in edu for x in undermatric):
                eduNo = 6
            else:
                eduNo = 7

            item['education'] = eduNo
        else:
            item['education'] = 7

        return item

class MaritalCleaner(object):
    def process_item(self, item, spider):
        if 'marital_status' in item and item['marital_status'] != None:
            marital_status = item['marital_status'].lower()
    
            if "unmarried" in marital_status:
                marital_status_no = 4
            elif "married" in marital_status:
                marital_status_no = 1
            elif "divorcee" in marital_status:
                marital_status_no = 3
            elif "widower" in marital_status:
                marital_status_no = 5
            elif "widow" in marital_status:
                marital_status_no = 2
            else:
                marital_status_no = 6

            item['marital_status'] = marital_status_no
        else:
            item['marital_status'] = 6

        return item
        
class ProfessionCleaner(object):
    def process_item(self, item, spider):
        
        professionList = { 
            'agriculturist':'Agriculturist',
            'advocate':'Lawyer',
            'adviser':'Advisor',
            'animal husbandry':'Animal husbandry',
            'author':'Author',
            'ayurvedic':'Ayurved',
            'bar-at-law':'Lawyer',
            'barrister-at-law':'Lawyer',
            'banker':'Banker',
            'bharatiya janata party':'Political worker',
            'builder':'Builder',
            'actor':'Film Artist',
            'building and road contractor':'Contractor',
            'business':'Business',
            'businessman':'Business',
            'businessperson':'Business',
            'chariman':'Chairman',
            'chartered accountant':'Chartered Accountant',
            'cine exhibitor':'Cine Exhibitor',
            'civil servant':'Civil Servant',
            'civil service':'Civil Servant',
            'comedian':'Comedian',
            'commerce':'Commerce',
            'communist':'Political worker',
            'congress':'Political worker',
            'consultant':'Consultant',
            'consulting':'Consultant',
            'c.p.i':'Political worker',
            'cultivator':'Cultivator',
            'defence services':'Defence',
            'diplomat':'Diplomat',
            'doctor':'Doctor',
            'economist':'Economist',
            'educationist':'Educationist',
            'editor':'Editor',
            'engineer':'Engineer',
            'entrepreneur':'Entrepreneur',
            'ex-governor':'Ex-Governor',
            'ex-commissioned officer':'Ex-Commissioned Officer',
            'exporter':'Exporter',
            'farming':'Farmer',
            'farmer':'Farmer',
            'film artist':'Film Artist',
            'artiste':'Artiste',
            'film producer':'Film Producer',
            'former judge':'Former Judge',
            'founder':'Founder',
            'founded':'Founder',
            'government servant':'Civil Servant',
            'harijan':'Political worker',
            'homeopath':'Homeopath',
            'horticulturist':'Horticulturist',
            'ias officer':'IAS Officer',
            'administrative service officer':'IAS Officer',
            'i.t. professional':'I.T. Professional',
            'imprison':'Imprisoned',
            'imprisonment':'Imprisoned',
            'industrialist':'Industrialist',
            'ips':'IPS Officer',
            'journalist':'Journalist',
            'l.i.c.':'L.I.C Agent',
            'lecturer':'Lecturer',
            'landlord':'Landlord',
            'lawyer':'Lawyer',
            'legal practice':'Lawyer',
            'legal practitioner':'Lawyer',
            'legislative assembly':'MLA',
            'literateur':'Literateur',
            'lok sabha':'Lok Sabha item',
            'll.b':'Lawyer',
            'managing director':'Managing Director',
            'merchant':'Merchant',
            'medical practitioner':'Medical Practitioner',
            'midwife':'Midwife',
            'military service':'Military',
            'millowner':'Mill owner',
            'mine owner':'Mine owner',
            'minister for education':'Education Minister',
            'minister':'Minister',
            'ministry of irrigation and power':'Ministry of Irrigation and Power',
            'musician':'Musician',
            'orator':'Orator',
            'performing artiste':'Artist',
            'pilot':'Pilot',
            'pleader':'Lawyer',
            'police service':'Police',
            'politics':'Politician',
            'political worker':'Political worker',
            'political':'Political worker',
            'politician':'Politician',
            'poet':'Poet',
            'poultry farming':'Poultry farming',
            'philanthropist':'Philanthropist',
            'physician':'Physician',
            'principal':'Principal',
            'professor':'Professor',
            'producer and director':'Producer and Director',
            'publisher':'Publisher',
            'public worker':'Public Worker',
            'real estate development':'Real Estate Development',
            'religious missonary':'Religious Missonary',
            'royal indian navy':'Royal Indian Navy',
            'secretary':'Secretary',
            'singer':'Singer',
            'social worker':'Social worker',
            'solicitor':'Lawyer',
            'sportsman':'Sportsperson',
            'sportsperson':'Sportsperson',
            'surgeon':'Surgeon',
            'teacher':'Teacher',
            'telangana praja samithi':'Political worker',
            'technologist':'Technologist',
            'trader':'Trader',
            'trade unionist':'Trade Union',
            'trade union':'Trade Union',
            'treasurer':'Treasurer',
            'vakil':'Lawyer',
            'veterinarian':'Veterinarian',
            'weaver':'Weaver',
            'widow':'Widow',
            'widower':'Widow',
            'writer':'Writer',
            'worked among the backward muslim communities':'Community helper',
            'zamindar':'Landlord',
            'industralist':'Industralist'
        }

        if 'profession' in item and item['profession'] != None:
            rawProfession = item['profession'].lower()
            profList = list()

            for prof in professionList:
                if prof in rawProfession:
                    profList.append(professionList[prof])
            
            item['profession'] = profList
        
        return item
        