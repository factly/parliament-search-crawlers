import pymongo
import json
client = pymongo.MongoClient("mongodb+srv://database-manager:s96kzwNljaYqg1Eb@cluster0-r4rsa.mongodb.net/test?retryWrites=true")
db = client.test
collection = db.lok_sabha
data = json.load(open("questions1.json","r"))
for question in data[100:120]:
    query = {"question_number": question["question_number"]}
    print(query)
    # print(question["question_number"], collection.find(query).count() > 0)