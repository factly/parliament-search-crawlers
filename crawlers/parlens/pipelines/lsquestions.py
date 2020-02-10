from scrapy.exceptions import DropItem
import pymongo
import json

class LSQuestionUploader(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        questionDict = list(db.all_questions.find({'qref': {'$regex': spider.session + "_",  '$options': 'i'}}, {'qref': 1}))
       
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

