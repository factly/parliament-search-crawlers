# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../var/folders/zq/b5ts9cfj21n_2v_vp7p8w4hr0000gn/T'))
	print(os.getcwd())
except:
	pass

#%%
import pymongo
import json
import pandas as pd
print ('Connecting to the mongo_database with details provided in file "config.cfg"')
config_file = open("config.cfg")
config = json.load(config_file)
client = pymongo.MongoClient(config["mongodb_uri"])
db = client[config["database"]]


#%%

#All parties upload into DB
df = pd.read_csv("parties_all.csv")
records = json.loads(df.T.to_json()).values()
#All parties 
db["partiesAll"].insert(records)

#%%
#Unique parties upload into DB
df = pd.read_csv("parties_unique.csv")
records = json.loads(df.T.to_json()).values()
#All parties 
db["politicalPartiesUnique"].insert(records)



