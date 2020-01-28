from scrapy.exceptions import DropItem
import pymongo
import json
import datetime
import time


class MinistryMatching(object):

    def open_spider(self, spider):    
        self.error_file = open("errors.log","a+")
        self.error_file.write("\n\n\n######## Lok Sabha Question Crawler "+str(datetime.datetime.now())+" ###########\n" )
        with open('./data/ministries.json', 'r', encoding='utf-8') as f:
            self.ministries = json.load(f)

    def process_item(self, item, spider):
        if item['ministry'].strip().upper() in self.ministries:
            item['ministry'] = self.ministries[item['ministry'].strip().upper()]
            return item
        else:
            missing_message = {
                'qref': item['qref'],
                'item': item['ministry'],
                'message': "ministry not found"
            }
            self.error_file.write(json.dumps(missing_message) + "\n")
            raise DropItem('ministry')

class RSAskedByMatching(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        self.members = list(db.rs_members.find({}, {'MID': 1, 'name': 1, 'terms': 1}))

        self.error_file = open("errors.log","a+")

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        questionByIDs = list()
        for asker in item['questionBy']:

            if 'Shri' in asker:
                newName = asker.split('Shri', 1)
            elif 'SHRI' in asker:
                newName = asker.split('SHRI', 1)
            elif 'Smt.' in asker:
                newName = asker.split('Smt.', 1)
            elif 'Dr.' in asker:
                newName = asker.split('Dr.', 1)
            elif 'DR.' in asker:
                newName = asker.split('DR.', 1)
            elif 'Prof.' in asker:
                newName = asker.split('Prof.', 1)
            elif 'Ms.' in asker:
                newName = asker.split('Ms.', 1)
            elif 'Miss' in asker:
                newName = asker.split('Miss', 1)
            elif 'Kumari' in asker:
                newName = asker.split('Kumari', 1)
            elif 'Sardar' in asker:
                newName = asker.split('Sardar', 1)
            elif 'Chaudhary' in asker:
                newName = asker.split('Chaudhary', 1)
            elif 'Ch.' in asker:
                newName = asker.split('Ch.', 1)
            elif 'Mahant' in asker:
                newName = asker.split('Mahant', 1)
            elif 'Mir' in asker:
                newName = asker.split('Mir', 1)
            else:
                missing_message = {
                    'qref': item['qref'],
                    'item': asker,
                    'message': "Prefix not found"
                }
                self.error_file.write(json.dumps(missing_message) + "\n")
                raise DropItem('name_prefix')


            askerList =  list(filter(lambda member: member['name'] == newName[1].strip().title(), self.members))
            if(len(askerList) == 1):
                questionByIDs.append(askerList[0]['MID'])
            else:
                missing_message = {
                    'qref': item['qref'],
                    'item': asker,
                    'message': str(len(askerList)) + " match for question by"
                }
                self.error_file.write(json.dumps(missing_message) + "\n")
                raise DropItem('question_by')

        item['questionBy'] = questionByIDs
        return item

class LSAskedByMatching(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        self.members = list(db.ls_members.find({}, {'MID': 1, 'name': 1, 'terms': 1}))

        self.error_file = open("errors.log","a+")
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        questionByIDs = list()
        for asker in item['questionBy']:
            
                name = " ".join(asker.split()).strip()

                askerList =  list(filter(lambda member: member['name'] == name, self.members))
                
                if(askerList and len(askerList) == 1):
                    questionByIDs.append(askerList[0]['MID'])
                else:
                    missing_message = {
                        'qref': item['qref'],
                        'item': asker,
                        'message': str(len(askerList)) + " match for question by"
                    }
                    self.error_file.write(json.dumps(missing_message) + "\n")
                    raise DropItem('question_by')
            
        item['questionBy'] = questionByIDs
        return item
        
class QuestionFinal(object):

    def process_item(self, item, spider):
        houseMapper = {
            'Lok Sabha': 1,
            'Rajya Sabha': 2
        }
        item['date'] = int(time.mktime(datetime.datetime.strptime(item['date'], "%d.%M.%Y").timetuple()) * 1000)
        item['house'] = houseMapper[item['house']]

        return item
