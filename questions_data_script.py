# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
print ('Initiating Script for Cleaning Questions Data\nImporting Libraries')


# %%
import json
import pymongo
import pandas as pd
from collections import defaultdict
from datetime import datetime
from itertools import permutations
from bs4 import BeautifulSoup


# %%
print ('Connecting to the mongo_database with details provided in file "config.cfg"')
config_file = open("config.cfg")
config = json.load(config_file)
client = pymongo.MongoClient(config["mongodb_uri"])
db = client[config["database"]]
questions_collection = db['lok_sabha_current_questions_html']
members_collection= db['cleanedMembers']
print ('the database connected now is',config["database"])
print ('the data collection loaded is:\n',members_collection,questions_collection)

# %% [markdown]
# # Reading collection as a pandas dataframe

# %%
df_q = pd.DataFrame(list(questions_collection.find({})))


# %%
df_m = pd.DataFrame(list(members_collection.find({})))

#%%

# Addding Ministry collection as a DataFrame

ministry_collection = db['ministry']
ministry = pd.DataFrame(list(ministry_collection.find({})))

# %%
#Function for Cleaning of Member Name in QuestionBy
def name_clean(member_name):
    member_name = member_name.strip()
    member_name = member_name.lstrip()
    member_name = member_name.rstrip()
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
        name = member_name.strip()
    return name


# %%
for i,row in df_q.iterrows():
    df_q.loc[i,"new_members"] = ['']


# %%

#Name Cleaning and Splitting the prefix
for i,row in df_q.iterrows():
    row = df_q.loc[i, "members"]
    new_row = []
    for j in row:
        j = name_clean(j)
        new_row.append(j)
    df_q.at[i,"new_members"] = new_row


# %% [markdown]
# # Date Cleaning

# %%
print ('Question Date Cleaning Started')
def date_clean(dat):
    date_formats = ["%d.%m.%Y", "%d %b %Y", "%B %d, %Y","%Y-%m-%d","%d %B,% %Y","%d %B %Y","%Y-%b-%d","%Y-%m-%d"]
    for date_format in date_formats:
        try:
            return datetime.strptime(dat,date_format).strftime("%Y-%m-%d")
        except:
            pass
    return dat


# %%
#Null Values to be blank
df_q = df_q.fillna('')


# %%
for i,row in df_q.iterrows():
    df_q.loc[i,"date"] = date_clean(row["date"])

print ('Date of Question Cleaning completed')
print("Number of records where date is not available is :", len(df_q.loc[df_q['date']==""]))


# %%
#new_question column
for i,row in df_q.iterrows():
    df_q.loc[i,"new_question"] = ['']

# %% [markdown]
## Making Question and Answer as a HTML
#HTML_Parsing of Question and storing in html

for i, row in df_q.iterrows():
    soup = ''
    row = df_q.loc[i,"text"]
    soup = BeautifulSoup(row,'html.parser')
    for x in soup.findAll("table", style ="margin-top: -15px;"):
        for y in x.find("td", {'class':'stylefontsize'}):
            df_q.at[i,"new_question"] = str(x.find("td", {'class':'stylefontsize'}))

#%%
#new_answer column
for i,row in df_q.iterrows():
    df_q.loc[i,"new_answer"] = ['']
            
#%% [markdown]
#HTML_Parsing of Answer and storing in html

for i, row in df_q.iterrows():
    soup = []
    row = df_q.loc[i,"text"]
    soup = BeautifulSoup(row,'html.parser')
    for x in soup.findAll("table", style ="margin-top: -15px;"):
        for y in x.findAll("td", {'class':'stylefontsize'})[1:]:
            df_q.at[i,"new_answer"] = str(y)

# %% [markdown]
# # Mapping of MemberName in QuestionBy Column to MemberID in cleanedMember

# %%
for i,row in df_q.iterrows():
    df_q.loc[i,"member_id"] = ['']


# %%
def MemberMatch(mem_name):
    value = []
    x = []
    y = []
    for i, row in df_m.iterrows():
        row = df_m.loc[i, "memberName"]
        mid = df_m.loc[i,"MID"]
        if mem_name == row:
            value = mid
            return value
        else:
            #add logging here! to check for what all instances the names didnt match!
            x = mem_name.split()
            y = row.split()
            if len(set(x) & set(y)) == len(x):
                value = mid
                return value
        


# %%
for i,row in df_q.iterrows():
    row = df_q.loc[i, "new_members"]
    new_row = []
    for j in row:
        new_row.append(MemberMatch(j))
    df_q.at[i,"member_id"] = new_row
#%%
#Mapping of Ministry ID MINID to ministry

for i, row in df_q.iterrows():
    row = df_q.loc[i,"ministry"]
    for j, val in ministry.iterrows():
        val = ministry.loc[j,'name']
        if row == val:
            df_q.at[i,"ministry"] = ministry.loc[j,'MINID']


# %% Creating a QID Column

df_q = df_q.reset_index()
df_q['QID'] = ''
df_q['QID'] = df_q.index + 100000

# %% [markdown]
# # creating dataframe with required columns

questions = df_q[['QID','link','question_type','english_pdf', 'hindi_pdf', 'date', 'ministry',
                 'subject','new_question', 'new_answer','member_id']]



# %%
questions = questions.rename(columns={"question_type":"type","member_id":"questionBy","date":"date",
                                     "new_question":"question","link":"link","english_pdf":"englishPdf","hindi_pdf":"hindiPdf",
                                     "ministry":"ministry","subject":"subject","new_answer":"answer"})

#%%
questions['house'] = 1


# %%
#Changing data type of date

questions['date'] = pd.to_datetime(questions['date'])

# %% [markdown]
# # adding questions dataframe to MongoDB Collection
records = json.loads(questions.T.to_json()).values()
db["cleanedQuestions"].insert(records)


# %%
questions.to_excel("questionsnow.xlsx")


# %%


