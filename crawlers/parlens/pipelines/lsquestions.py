from scrapy.exceptions import DropItem
import pymongo
import json

class QuestionByCleaning(object):
    def process_item(self, item, spider):
        newQuestionBy = list()
        for asker in item['questionBy']:
            askerNew = asker.replace(",", " ").strip()
            askerNew = " ".join(askerNew.split()).strip()
        
            newQuestionBy.append(askerNew.upper())
           

        item['questionBy'] = newQuestionBy
        
        return item

# convert QuestionBy's LSID to MID
class QuestionByMatching(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        members = list(db.members.find({'terms.house': 1, 'terms.session': int(spider.session)}, {'MID': 1, 'name': 1}))
        
        print("***********************MEMBER LIST START***********************")
        print(members)
        print("***********************MEMBER LIST END***********************")
        self.LSIDtoMID = dict()
        
        for member in members:
            self.LSIDtoMID[member['name'].upper()] = member['MID']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        questionByIDs = list()
        
        for asker in item['questionBy']:
            if(asker in self.LSIDtoMID):
                questionByIDs.append(self.LSIDtoMID[asker])
            else:
                missing_message = {
                    'qref': item['qref'],
                    'item': asker,
                    'message': "LSID not found in LSIDtoMID"
                }
                spider.error.write(json.dumps(missing_message) + "\n")
            
        item['questionBy'] = questionByIDs
        return item

# remove already existing question based on qref (session_questionID)
class QuestionUploader(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        questionDict = list(db.questions.find({'qref': {'$regex': spider.session + "_",  '$options': 'i'}}, {'qref': 1}))
       
        self.questionsPresent = list()
        
        for each in questionDict:
            self.questionsPresent.append(each['qref']) 

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
       
        if(item['qref'] not in self.questionsPresent):
            return item
        else:
            raise DropItem('already_there')

