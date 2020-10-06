from scrapy.exceptions import DropItem
import pymongo
import json

# based on qref remove already existing questions
class DuplicateCleaner(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        questionDict = list(db.questions.find({'qref': {'$regex': spider.session + "_" + spider.questionType.strip(),  '$options': 'i'}}, {'qref': 1}))
       
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

# remove prefix from questionBy
class AskedByCleaning(object):
    def process_item(self, item, spider):
        newQuestionBy = list()
        for asker in item['questionBy']:
            if 'Shri' in asker:
                newName = asker.split('Shri', 1)[1]
            elif 'SHRI' in asker:
                newName = asker.split('SHRI', 1)[1]
            elif 'Smt.' in asker:
                newName = asker.split('Smt.', 1)[1]
            elif 'Dr.' in asker:
                newName = asker.split('Dr.', 1)[1]
            elif 'DR.' in asker:
                newName = asker.split('DR.', 1)[1]
            elif 'Prof.' in asker:
                newName = asker.split('Prof.', 1)[1]
            elif 'Ms.' in asker:
                newName = asker.split('Ms.', 1)[1]
            elif 'Miss' in asker:
                newName = asker.split('Miss', 1)[1]
            elif 'Kumari' in asker:
                newName = asker.split('Kumari', 1)[1]
            elif 'Sardar' in asker:
                newName = asker.split('Sardar', 1)[1]
            elif 'Chaudhary' in asker:
                newName = asker.split('Chaudhary', 1)[1]
            elif 'Ch.' in asker:
                newName = asker.split('Ch.', 1)[1]
            elif 'Mahant' in asker:
                newName = asker.split('Mahant', 1)[1]
            elif 'Mir' in asker:
                newName = asker.split('Mir', 1)[1]
            else:
                newName = asker
                missing_message = {
                    'qref': item['qref'],
                    'item': asker,
                    'message': "Prefix not found"
                }
                spider.error.write(json.dumps(missing_message) + "\n")
                
            newQuestionBy.append(" ".join(newName.split()).strip().title())
        
        item['questionBy'] = newQuestionBy

        return item

# match questionBy name with db name
class QuestionByMatching(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        self.members = list(db.members.find({}, {'MID': 1, 'name': 1, 'terms': 1}))

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        questionByIDs = list()
        for asker in item['questionBy']:
            askerList =  list(filter(lambda member: member['name'] == asker, self.members))
            if(len(askerList) == 1):
                questionByIDs.append(askerList[0]['MID'])
            else:
                missing_message = {
                    'qref': item['qref'],
                    'item': asker,
                    'message': str(len(askerList)) + " match for question by"
                }
                spider.error.write(json.dumps(missing_message) + "\n")

        item['questionBy'] = questionByIDs if len(questionByIDs) > 0 else item['questionBy']
        return item