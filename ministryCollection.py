#%%
import pymongo
import json
import pandas as pd
import numpy as np
print ('Connecting to the mongo_database with details provided in file "config.cfg"')
config_file = open("config.cfg")
config = json.load(config_file)
client = pymongo.MongoClient(config["mongodb_uri"])
db = client[config["database"]]

#%%

df = pd.read_excel("ministries.xlsx")



# %%

# %%
#adding data to json
records = json.loads(df.T.to_json()).values()

# %%
#adding data to Mongo db

db["ministry"].insert(records)


# %%
