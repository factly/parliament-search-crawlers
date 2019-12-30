#%% [markdown]
## Cleaning of Rajyasabha Members Data
## Source : https://data.gov.in/resources/current-members-rajya-sabha-30-november-2017-english
#loading libraries
import pandas as pd
import json
from word2number import w2n
import pymongo
import numpy as np

# %%

config_file = open("config.cfg")
config = json.load(config_file)
client = pymongo.MongoClient(config["mongodb_uri"])
db = client[config["database"]]
collection = db["rsMembers"]
geography = db['geography']
parties_all = db['partiesAll']
political_parties = db['politicalPartiesUnique']

# %%
# Reading the data
dfrs = pd.read_excel("rajyasabhamembers.xlsx")
par = pd.DataFrame(list(parties_all.find({})))
df_p = pd.DataFrame(list(political_parties.find({})))
df_g = pd.DataFrame(list(geography.find({})))

# %%
# Creating a dataframe with required columens

dfrs = dfrs[['Member Name', 'Gender', 'Email ID','Whether Minister', 'Term Start Date',
       'Term End Date', 'State Name', 'Party Name', 'Date of Birth', 'Place of Birth', 'Maritial Status',
       'No. of Sons', 'No. of Daughters',
       'Educational Qualifications', 'Other Profession(s)']]

# %% [markdown]
# Cleaning of name

def name_clean(member_name):
    member_name = member_name.strip()
    if 'Sh.' in member_name:
        member_list = member_name.split('Sh.')
        name = 'Sh.'+" "+member_list[-1]+" "+' '.join(member_list[:-1])
    elif 'Smt.' in member_name:
        if "," in member_name: 
            name_list = member_name.split(',')
            if len(name_list) >= 2:
                name = name_list[1].strip()+" "+name_list[0].strip()
                name = name.replace("  "," ").replace('\xa0','')
        else:
            member_list = member_name.split('Smt.')
            name = 'Smt.'+" "+member_list[-1]+" "+' '.join(member_list[:-1]).strip(',')
    elif ',' in member_name:
        name_list = member_name.split(',')
        if len(name_list) >= 2:
            name = name_list[1].strip()+" "+name_list[0].strip()
            name = name.replace("  "," ").replace('\xa0','')
    else:
        name = member_name
    return name

def namesplit(value):
    value = value.split(" ")
    return value


#%%

for i,row in dfrs.iterrows():
    dfrs.loc[i,"Member Name"] = name_clean(row["Member Name"])
#%%
#Splitting of Name to prefix and name as different columns
dfrs["prefix"] = ""
dfrs["new_name"] = ""

for i, row in dfrs.iterrows():
    dfrs.loc[i,"prefix"] = namesplit(row["Member Name"])[0]
    dfrs.loc[i,"new_name"] = " ".join(namesplit(row["Member Name"])[1:]).strip()

# %% [markdown]
## Education Cleaning
#Defining a new column

dfrs['edu_level'] = ""

#Function
def edu_clean(edu):
    #list of values for education level for the function to check for
    phd =['Ph.D.','Ph. D', 'Doctorate']
    ug = ['Engg','Bachelor of Engineering','B. A.','B.A','B.Com','B.Sc','L.L.B','B.E','B.B.M',
          'B.B.A','M.B.B.S','B.M.S.','C.A', 'B. Com','B. Sc','Undergraduate','Law','B. Tech.',
          'Universit','B.Tech.','B. Tech','Graduat']
    pg = ['LL.M','M.A','M.Sc','M.Com','M.B.A','M.D','M.D.M','M.E','M.L','L.L.M','Graduate','Post Graduate','M. Com','Master','Masters']
    inter =['Inter','Intermediate','Higher Secondary','PUC']
    school = ['High School', 'S.S.C', 'School','school']
    undermatric = ['Under Matriculate','Under-Matric','Under Matric']
    matric=['Matric','Matriculation']
    
    if any(x in edu for x in phd):
        return 1
    elif any(x in edu for x in pg):
        return 2
    elif any(x in edu for x in ug):
        return 3
    elif any(x in edu for x in inter):
        return 4
    elif any(x in edu for x in school):
        return 5
    elif any(x in edu for x in matric):
        return 5
    elif any(x in edu for x in undermatric):
        return 6
    elif "Diploma" in edu:
        return 4
    else:
        return 6

#implementing education level cleaning
for i,row in dfrs.iterrows():
    dfrs.loc[i,"edu_level"] = edu_clean(str(row["Educational Qualifications"]))

print("Number of records where Education Level is not available is:", len(dfrs.loc[dfrs['edu_level']==""]))



# %%
# Dictionary of professions
prof_dict = {
    "Agriculturist" : "Agriculturist",
    "Agriculture":"Agriculturist",
    "Actor":"Actor",
    "Artist":"Actor",
    "Artiste":"Actor",
    "Artiste (Film)":"Actor",
    "agriculturist" : "Agriculturist",
    "Advocate" : "Lawyer",
    "Adviser" : "Advisor",
    "Animal husbandry" : "Animal husbandry",
    "author" : "Author",
    "Ayurvedic" : "Ayurved",
    "Bar-at-Law" : "Lawyer",
    "Barrister-at-Law" : "Lawyer",
    "Banker" : "Banker",
    "Bharatiya Janata party" : "Political worker",
    "Builder" : "Builder",
    "Building and Road Contractor" : "Contractor",
    "Businessman" : "Business",
    "Business":"Business",
    "Businessperson" : "Business",
    "Chariman" : "Chairman",
    "Chartered Accountant" : "Chartered Accountant",
    "Cine Exhibitor" : "Cine Exhibitor",
    "Civil Servant" : "Civil Servant",
    "Civil Service" : "Civil Servant",
    "Civil service" : "Civil Servant",
    "Comedian" : "Comedian",
    "Commerce" : "Commerce",
    "Communist" : "Political worker",
    "Congress" : "Political worker",
    "Consultant" : "Consultant",
    "Consulting" : "Consultant",
    "C.P.I" : "Political worker",
    "Cultivator" : "Cultivator",
    "Defence Services" : "Defence",
    "Diplomat" : "Diplomat",
    "Doctor" : "Doctor",
    "Economist" : "Economist",
    "educationist" : "Educationist",
    "Educationist" : "Educationist",
    "editor" : "Editor",
    "Editor" : "Editor",
    "Engineer" : "Engineer",
    "Entrepreneur" : "Entrepreneur",
    "Ex-Governor" : "Ex-Governor",
    "Ex-Commissioned Officer" : "Ex-Commissioned Officer",
    "Exporter" : "Exporter",
    "Farming" : "Farmer",
    "Farmer" : "Farmer",
    "Film Artist" : "Film Artist",
    "Film Producer" : "Film Producer",
    "Former Judge" : "Former Judge",
    "Founder" : "Founder",
    "Founded" : "Founder",
    "Government Servant" : "Civil Servant",
    "Harijan" : "Political worker",
    "Homeopath" : "Homeopath",
    "Horticulturist" : "Horticulturist",
    "Hockey Player" : "Hockey Player",
    "IAS Officer" : "IAS Officer",
    "Administrative Service Officer" : "IAS Officer",
    "I.T. Professional" : "I.T. Professional",
    "Imprison" : "Imprisoned",
    "imprisonment" : "Imprisoned",
    "Industrialist" : "Industrialist",
    "IPS" : "IPS Officer",
    "Journalist" : "Journalist",
    "Journalism":"Journalist",
    "L.I.C." : "L.I.C Agent",
    "Lecturer" : "Lecturer",
    "Landlord" : "Landlord",
    "lawyer" : "lawyer",
    "Lawyer" : "Lawyer",
    "legal practice" : "Lawyer",
    "Legal practitioner" : "Lawyer",
    "Legal Practitioner" : "Lawyer",
    "Legislative Assembly" : "MLA",
    "Literateur" : "Literateur",
    "Lok Sabha" : "Lok Sabha member",
    "LL.B" : "Lawyer",
    "Managing Director" : "Managing Director",
    "Merchant" : "Merchant",
    "merchant" : "Merchant",
    "Medical Practitioner" : "Medical Practitioner",
    "Midwife" : "Midwife",
    "Military Service" : "Military",
    "Millowner" : "Mill owner",
    "Mine owner" : "Mine owner",
    "Minister for Education" : "Education Minister",
    "Minister" : "Minister",
    "Ministry of Irrigation and Power" : "Ministry of Irrigation and Power",
    "Musician" : "Musician",
    "Orator" : "Orator",
    "Performing Artiste" : "Artist",
    "Pilot" : "Pilot",
    "Pleader" : "Lawyer",
    "Police Service" : "Police",
    "Politics" : "Politician",
    "Political worker" : "Political worker",
    "Political Worker" : "Political worker",
    "Political" : "Political worker",
    "Politician" : "Politician",
    "Poet" : "Poet",
    "Poultry farming" : "Poultry farming",
    "Philanthropist" : "Philanthropist",
    "Physician" : "Physician",
    "Principal" : "Principal",
    "Professor" : "Professor",
    "professor" : "Professor",
    "Producer and Director" : "Producer and Director",
    "Practice in Optometry (refractionist)": "Opthomologist",
    "publisher" : "Publisher",
    "Public Worker" : "Public Worker",
    "Public worker" : "Public Worker",
    "Real Estate Development" : "Real Estate Development",
    "Religious Missonary" : "Religious Missonary",
    "Religious missonary" : "Religious Missonary",
    "Royal Indian Navy" : "Royal Indian Navy",
    "Secretary" : "Secretary",
    "Singer" : "Singer",
    "Social Worker" : "Social worker",
    "Social worker" : "Social worker",
    "Solicitor" : "Lawyer",
    "Sportsman" : "Sportsperson",
    "Sportsperson" : "Sportsperson",
    "Surgeon" : "Surgeon",
    "teacher" : "Teacher",
    "Teacher" : "Teacher",
    "Telangana Praja Samithi" : "Political worker",
    "Technologist" : "Technologist",
    "Trader" : "Trader",
    "Trade Unionist" : "Trade Union",
    "Trade Union" : "Trade Union",
    "Treasurer" : "Treasurer",
    "Vakil" : "Lawyer",
    "Veterinarian" : "Veterinarian",
    "Weaver" : "Weaver",
    "Widow" : "Widow",
    "widower" : "Widow",
    "Writer" : "Writer",
    "writer" : "Writer",
    "Worked among the backward Muslim communities" : "Community helper",
    "Zamindar" : "Landlord",
    "Quiz Master/Author": "Quiz Master"
}


# %%
# Copy profession values to a new column
dfrs["new_profession"] = dfrs['Other Profession(s)']
# Splitting the string into a series
dfrs.new_profession = dfrs.new_profession.astype(str)

# Removing return carriage and newline
dfrs.new_profession = dfrs.new_profession.str.replace(r'\r\n', '')
# Removing _x000D_ in the string series
dfrs.new_profession = dfrs.new_profession.str.replace(r'_x000D_', '')
# Replacing multiple spaces with a single space
dfrs.new_profession = dfrs.new_profession.str.replace(r'\s+', ' ')

# Making new_profession in the format ['Profession1', 'Profession2'] format
sent_set_list = []
for sent in dfrs.new_profession:
    if (sent == 'nan'):
        sent_set_list.append([])
        continue
    string_prof = set()
    for (prof, prof_name) in prof_dict.items():
        if prof in sent:
            string_prof.add(prof_name)
    sent_set_list.append(list(string_prof))

dfrs.new_profession = sent_set_list
count = 0
for cnan in sent_set_list:        
    if 'nan' in cnan:
        count +=1
print ("Number of records where Profession is not available is:", count)


# %%
# Changing gender to numeric values

for i, row in dfrs.iterrows():
    row = dfrs.loc[i, "Gender"]
    if row == "Male":
        dfrs.at[i,"Gender"] = 2
    if row == "Female":
        dfrs.at[i,"Gender"] = 1
    if row == "Third Gender":
        dfrs.at[i,"Gender"] = 3

#%%
dfrs['Term Start Date'] = pd.to_datetime(dfrs['Term Start Date'])
dfrs['Term End Date'] = pd.to_datetime(dfrs['Term End Date'])

#%%
#Defining terms column in dfrs

for i, row in dfrs.iterrows():
    dfrs.loc[i,"terms"] = ['']

#%%
#defining terms structure
for i, row in dfrs.iterrows():
# Creating terms dictionary
    t = dict()
    t['0'] = dict()
    t['0']['session'] = np.nan
    t['0']['party'] = dfrs["Party Name"][i]
    t['0']['geography'] = dfrs['State Name'][i]
    t['0']['house'] = 2
    t['0']['from'] = dfrs['Term Start Date'][i].year
    t['0']['to'] = dfrs['Term End Date'][i].year
    dfrs['terms'][i] = t

#%%
# # Term Details : session, Party_id, GeographyID, house
for i, row in dfrs.iterrows():
    row = dfrs.loc[i,"terms"]
    for key, value in row.items():
        for k, l in value.items():
            for k, l in par.iterrows():
                l = par.loc[k,"party_raw"]
                if value['party'] == l:
                    value['party'] = par.loc[k,"name"]
            for m, n in df_g.iterrows():
                n = df_g.loc[m,"name"]
                if value['geography'] == n and df_g.loc[m,'type'] == 'state':
                    value['geography'] = df_g.loc[m,"GID"]

# Party ID Mapping           
for i, row in dfrs.iterrows():
    row = dfrs.loc[i,"terms"]
    for key, value in row.items():
        for k, l in value.items():
            for o,p in df_p.iterrows():
                p = df_p.loc[o,"name"]
                if value['party'] == p:
                    value['party'] = df_p.loc[o,"PID"]

#%%

dfrs[['No. of Sons', 'No. of Daughters']] = dfrs[['No. of Sons', 'No. of Daughters']].fillna('0')
dfrs[['No. of Sons', 'No. of Daughters']] = dfrs[['No. of Sons', 'No. of Daughters']].astype(str)
#%%
for i,row in dfrs.iterrows():
    dfrs.loc[i,"sons"] = ''
    dfrs.loc[i,'daughters'] = ''
#%%
#Sons
for i, row in dfrs.iterrows():
    row = dfrs.loc[i,"No. of Sons"]
    if row == '0':
        dfrs.at[i,"sons"] = 0
    elif type(row) == int:
        dfrs.at[i,"sons"] = row
    else:
        dfrs.at[i,"sons"] = w2n.word_to_num(row)
#%%
#Daughters
for i, row in dfrs.iterrows():
    row = dfrs.loc[i,"No. of Daughters"]
    if row == '0':
        dfrs.at[i,"daughters"] = 0
    elif type(row) == int:
        dfrs.at[i,"daughters"] = row
    else:
        dfrs.at[i,"daughters"] = w2n.word_to_num(row)


#%%
## Creating a dataframe for rajya sabha members