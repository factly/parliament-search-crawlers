# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # LS Sitting Members Data Cleaning & Data Updating Script

# %%
print ('Initiating Script for Cleaning Lok Sabha Members Data\nImporting Libraries')
import json
import pymongo
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime, timezone
from itertools import permutations
import dateutil.parser as parser

# %% [markdown]
# #Connecting to the Mongo Database and respective collections

# %%
print ('Connecting to the mongo_database with details provided in file "config.cfg"')
config_file = open("config.cfg")
config = json.load(config_file)
client = pymongo.MongoClient(config["mongodb_uri"])
db = client[config["database"]]
members_collection = db['current_ls_members']
geography = db['geography']
parties_all = db['partiesAll']
political_parties = db['politicalPartiesUnique']
archive_members = db["archive_ls_members"]
print ('the database connected now is',config["database"])
print ('the data collection loaded is:\n',members_collection)


# %%
#mongodb collections to pandas dataframes for members, geography and parties
df_m = pd.DataFrame(list(members_collection.find({})))
df_g = pd.DataFrame(list(geography.find({})))
par = pd.DataFrame(list(parties_all.find({})))
df_a = pd.DataFrame(list(archive_members.find({})))
df_p = pd.DataFrame(list(political_parties.find({})))



# %% [markdown]
# # Defining Functions for data cleaning

# %%
#Name Cleaning Function "name_clean()"
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

#Gender creating Function "get_gender()"
def get_gender(name):
    title = name
    female_titles = [
        'Begam',
        'Begum',
        'Devi',
        'Dr.(Kum.)',
        'Dr.(Smt.)',
        'Dr.(Smt.)Chellamalla',
        'Her',
        'Km.',
        'Kum.',
        'Kumari',
        'Maharani',
        'Ms.',
        'Prof.(Smt.)',
        'Rajkumari',
        'Rajmata',
        'Rajmata(Jodhpur)',
        'Rani',
        'Sadhvi',
        'Sardarni',
        'Smt',
        'Smt.',
        'Sushree',
        'Sukanta Majumdar',
        'Rita Bahuguna Joshi',
        'Heena Vijaykumar Gavit',
        'Bharatiben Dhirubhai Shyal',
        'Beesetti Venkata Satyavathi',
        'Dr. Bharti Pravin Pawar',
        'Dr. T. Sumathy'
    ]
    male_titles = [
        '(Pandit)',
        'Acharya',
        'Adv.',
        'Baba',
        'Babu',
        'Capt.',
        'Capt.(Retd.)',
        'Captain',
        'Ch.',
        'Chaudhari',
        'Chaudhary',
        'Chaudhri',
        'Chaudhry',
        'Choudari',
        'Choudhary',
        'Choudhury',
        'Chowdhary',
        'Chowdhry',
        'Chowdhury',
        'Col.',
        'Dr.Maharaja',
        'Father',
        'General',
        'H.H.',
        'H.H.Maharaja',
        'Haji',
        'Kazi',
        'Kh.',
        'Kunwar',
        'Lala',
        'Lt.',
        'Lt.Col.',
        'Mahant',
        'Maharajkumar',
        'Maj',
        'Maj.',
        'Maj.Gen.',
        'Major',
        'Major-General',
        'Maulana',
        'Mohammad',
        'Mohd.',
        'Motilal',
        'Mulla',
        'Pandit',
        'Purohit',
        'Qazi',
        'Raja',
        'Rt.',
        'Sardar',
        'Seth',
        'Shaikh',
        'Shri',
        'Shriman',
        'Swami',
        'Syed',
        'Thakur',
        'Thiru',
        'Vaidya',
        'Visharad',
        'Farooq Abdullah',
        'Vishnu Prasad',
        'Radhakrishna Vikhepatil',
        'Shashi Tharoor',
        'Maharaj',
        'Dr. Alok Kumar Suman',
        'Dr. (Prof.) Kirit Premjibhai Solanki',
        'Satya Pal Singh',
        'Dr. Jitendra Singh',
        'Dr. Amar Singh',
        'Dr. Sanjeev Kumar Singari',
        'Dr. Shrikant Eknath Shinde',
        'Dr. Mahesh Sharma',
        'Dr. Arvind Kumar Sharma',
        'Dr. Jadon Chandra Sen',
        'Dr. Subhas Sarkar',
        'Prof. Sougata Ray',
        'Dr. Jayanta Kumar Roy',
        'Dr. Rajdeep Roy',
        'Dr. Gaddam Ranjith Reddy',
        'Rao Inderjit Singh',
        'Dr. Manoj Rajoria',
        'Dr. Ranjan Singh Rajkumar',
        'Dr. Lorho S. Pfoze',
        'Dr. K. C. Patel',
        'Dr. Mahendra Nath Pandey',
        'Dr. T. R. Paarivendhar',
        'Dr. Ramesh Pokhriyal Nishank',
        'Dr. Mahendrabhai Kalubhai Munjpara',
        'Dr. Pritam Gopinath Munde',
        'Dr. Sanghamitra Maurya',
        'Dr. Jaisiddeshwar Shivacharya Mahaswamiji',
        'Dr. Virendra Kumar',
        'Dr. Amol Ramsing Kolhe',
        'Prof. (Dr.) Ram Shankar Katheria',
        'Dr. V. Kalanidhi',
        'Dr. Mohammad Jawed',
        'Dr. K. Jayakumar',
        'Dr. Sanjay Jaiswal',
        'Dr. Umesh G. Jadhav',
        'Dr. Harsh Vardhan',
        'Dr. S.T. Hasan',
        'Vijay Kumar Singh (Retd.) General (Dr.)',
        'Dr. Nishikant Dubey',
        'Dr. A. Chellakumar',
        'Dr. Dhal Singh Bisen',
        'Dr. Subhash Ramrao Bhamre',
        'Dr. Sanjeev Kumar Balyan',
        'Prof. S.P. Singh Baghel',
        'Dr. Krishna Pal Singh Yadav',
        'Dr. DNV Senthilkumar S.'
    ]
    if any(x in title for x in female_titles):
        return 1
    if any(x in title for x in male_titles):
        return 2
    else:
        return ""

#Date Cleaning Function "date_clean()"

def date_clean(dat):
    date_formats = ["%d.%m.%Y", "%d %b %Y", "%B %d, %Y","%Y-%m-%d","%d %B,% %Y","%d %B %Y","%Y-%b-%d","%Y-%m-%d"]
    for date_format in date_formats:
        try:
            return datetime.strptime(dat,date_format).strftime("%Y-%m-%d")
        except:
            pass
    return dat

#education cleaning Function "edu_clean()"

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

#Name Split Function

def namesplit(value):
    value = value.split(" ")
    return value

# %%
#implementing name_cleaning
for i,row in df_m.iterrows():
    df_m.loc[i,"name"] = name_clean(row["name"])

print ('gender cleaning')
#adding gender column
df_m["gender"] = ""
#implementing gender cleaning
for i,row in df_m.iterrows():
    df_m.loc[i,"gender"] = get_gender(row["name"])
print("Number of records where Gender is not available is :", len(df_m.loc[df_m['gender']==""]))

#Implementing date of birth Cleaning
for i,row in df_m.iterrows():
    df_m.loc[i,"dob"] = date_clean(row["dob"])

print ('Date of Birth Cleaning completed')
print("Number of records where DOB is not available is :", len(df_m.loc[df_m['dob']==""]))

#implementing education level cleaning
df_m["edu_level"] = ""
for i,row in df_m.iterrows():
    df_m.loc[i,"edu_level"] = edu_clean(str(row["education"]))

print("Number of records where Education Level is not available is:", len(df_m.loc[df_m['edu_level']==""]))

#%%
#Splitting of Name to prefix and name as different columns
df_m["prefix"] = ""
df_m["new_name"] = ""

for i, row in df_m.iterrows():
    df_m.loc[i,"prefix"] = namesplit(row["name"])[0]
    df_m.loc[i,"new_name"] = " ".join(namesplit(row["name"])[1:]).strip()

# %% [markdown]
# # Profession Cleaning

# %%
# Dictionary of professions
prof_dict = {
    "Agriculturist" : "Agriculturist",
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
    "IAS Officer" : "IAS Officer",
    "Administrative Service Officer" : "IAS Officer",
    "I.T. Professional" : "I.T. Professional",
    "Imprison" : "Imprisoned",
    "imprisonment" : "Imprisoned",
    "Industrialist" : "Industrialist",
    "IPS" : "IPS Officer",
    "Journalist" : "Journalist",
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
    "Zamindar" : "Landlord"
}


# %%
# Copy profession values to a new column
df_m["new_profession"] = df_m['profession']
# Splitting the string into a series
df_m.new_profession = df_m.new_profession.astype(str)

# Removing return carriage and newline
df_m.new_profession = df_m.new_profession.str.replace(r'\r\n', '')
# Removing _x000D_ in the string series
df_m.new_profession = df_m.new_profession.str.replace(r'_x000D_', '')
# Replacing multiple spaces with a single space
df_m.new_profession = df_m.new_profession.str.replace(r'\s+', ' ')

# Making new_profession in the format ['Profession1', 'Profession2'] format
sent_set_list = []
for sent in df_m.new_profession:
    if (sent == 'nan'):
        sent_set_list.append([])
        continue
    string_prof = set()
    for (prof, prof_name) in prof_dict.items():
        if prof in sent:
            string_prof.add(prof_name)
    sent_set_list.append(list(string_prof))

df_m.new_profession = sent_set_list
count = 0
for cnan in sent_set_list:        
    if 'nan' in cnan:
        count +=1
print ("Number of records where Profession is not available is:", count)

# %% [markdown]
# # Email Cleaning

# %%
#Defining a new column for cleaned email id's as a array of lists
for i,row in df_m.iterrows():
    df_m.loc[i,"new_email"] = ['']
    
#Function for replacing the [AT] and [DOT] in the emails
dic = {
    "[AT]" : "@",
    "[DOT]" : ".",
    "NIL" : ""
    }
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

#Iterating over each row of emails and appending them to the new_email
for i,row in df_m.iterrows():
    row = df_m.loc[i, "email"]
    new_row = []
    for j in row:
        j.replace(",","")
        j.strip()
        new_row.append(replace_all(j,dic))
    df_m.at[i,"new_email"] = new_row

print("Number of records where Email is not available is:", len(df_m.loc[df_m['new_email']==""]))

# %% [markdown]
# # Term Details : session, Party_id, GeographyID, house

# %%
for i, row in df_m.iterrows():
    row = df_m.loc[i,"terms"]
    for j in row:
        for key, value in j.items():
            for k, l in par.iterrows():
                l = par.loc[k,"party_raw"]
                if j['party'] == l:
                    j['party'] = par.loc[k,"name"]
            for m, n in df_g.iterrows():
                n = df_g.loc[m,"name"]
                if j['geography'] == n and df_g.loc[m,'type']=='constituency':
                    j['geography'] = df_g.loc[m,"GID"]


for i, row in df_m.iterrows():
    row = df_m.loc[i,"terms"]
    for j in row:
        for key, value in j.items():
            for o,p in df_p.iterrows():
                p = df_p.loc[o,"name"]
                if j['party'] == p:
                    j['party'] = df_p.loc[o,"PID"]

#%%
# Coverting values in marital status to categories:
for i, row in df_m.iterrows():
    row = df_m.loc[i, "marital_status"]
    if row == "Married" or row == "MARRIED":
        df_m.at[i, "marital_status"] = 1
    if row == "Widow":
        df_m.at[i, "marital_status"] = 2
    if row == "Divorcee":
        df_m.at[i, "marital_status"] = 3
    if row == "Unmarried":
        df_m.at[i, "marital_status"] = 4
    if row == "Widower":
        df_m.at[i, "marital_status"] = 5

# %% [markdown]
# # creating dataframe with required columns
# 

# %%
members = df_m[['_id','prefix','new_name','name','gender','dob','birth_place','marital_status',
                'sons','daughters','new_email','phone','new_profession','edu_level','terms']]


# %%
members = members.rename(columns={"_id":"MID",'name':'memberName',"new_email":"email","new_name":"name",
                                  "new_profession":"profession","edu_level":"education",
                                 "gender":"gender","birth_place":"birthPlace","marital_status":"maritalStatus",
                                 "dob":"dob","sons":"sons","daughters":"daughters","phone":"phone",
                                 "terms":"terms"})


# %%
for i,row in members.iterrows():
    members.at[i,"expertise"] = ['']

# %%
## Changing the datatypes
members['MID'] = members['MID'].astype(int)
members['sons'] = members['sons'].astype(np.float64)
members['daughters'] = members['daughters'].astype(np.float64)
members['dob'] = pd.to_datetime(members['dob'])
members['education']= members['education'].astype(np.float64)
members['maritalStatus'] = members['maritalStatus'].astype(np.float64)
members['gender'] = members['gender'].astype(np.float64)
    
# %% [markdown]
# Run this only after you check the dataframe

# %% [markdown]
# # Adding the members dataframe to MongoDb Collection
records = json.loads(members.T.to_json(force_ascii= False)).values()
db["cleanedMembers"].insert(records)


# %%
members.to_excel("Members.xlsx")


# %%
members


# %%


