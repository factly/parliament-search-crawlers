from scrapy.exceptions import DropItem
import pymongo
import json
import datetime
import time

class DOBCleaner(object):
    def process_item(self, item, spider):
        if 'dob' in item and item['dob'] != None:
            item['dob'] = int(time.mktime(datetime.datetime.strptime(item['dob'], "%d %b %Y").timetuple()) * 1000)
        else:
            item['dob'] = None

        return item
    
class EmailCleaner(object):
    def process_item(self, item, spider):
        if 'email' in item and len(item['email']) > 0:
            newEmailList = list()
            for each in item['email']:
                newEmailList.append(each.replace("[DOT]", ".").replace("[AT]", "."))
            item['email'] = newEmailList
        else:
            item['email'] = list()

        return item

class ChildrenCleaner(object):
    def process_item(self, item, spider):
        if 'sons' in item and item['sons'] != None:
            item['sons'] = int(item['sons'])
        else:
            item['sons'] = None

        if 'daughters' in item and item['daughters'] != None:
            item['daughters'] = int(item['daughters'])
        else:
            item['daughters'] = None

        return item

class LSDuplicateCleaner(object):
    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        questionDict = list(db.all_members.find({'terms.session': spider.session }, {'LSID': 1}))
       
        self.membersPresent = list()
        
        for each in questionDict:
            self.membersPresent.append(each['LSID'])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
       
        if(item['LSID'] not in self.membersPresent):
            return item
        else:
            raise DropItem('already_there')

class GeoTermCleaner(object):
    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        constituencies = list(db.all_geography.aggregate([
            {
                '$match': {
                    'type': 'constituency'
                }
            },
            {
                '$lookup': {
                    'from': 'all_geography',
                    'localField': 'parent',
                    'foreignField': 'GID',
                    'as': 'parent'
                }
            },
            {
                '$unwind': '$parent'
            }
        ]))
       
        self.constituenciesDict = dict()
        for each in constituencies:
            self.constituenciesDict[each['name'] + "#" + each['parent']['name'] + "#" + each['category']] = each['GID']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        constituencyKey = item['geography'] + "#" + item['state'] + "#" + item['geography_type']
        if(constituencyKey in self.constituenciesDict):
            item['geography'] = self.constituenciesDict[constituencyKey]
            return item
        else:
            raise DropItem('geo_not_found')

class GeoPartyCleaner(object):
    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        parties = list(db.all_parties.find({}))
       
        self.partiesDict = dict()
        for each in parties:
            self.partiesDict[each['name']] = each['PID']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        
        if(item['party'] in self.partiesDict):
            item['party'] = self.partiesDict[item['party']]
            return item
        else:
            raise DropItem('party_not_found')

class TermConstructor(object):
    def open_spider(self, spider):    
        with open('./data/sessiondate.json', 'r', encoding='utf-8') as f:
            sessiondates = json.load(f)

        self.from_to = sessiondates[str(spider.session)]
    def process_item(self, item, spider):
        item['term'] = {
            'geography': item['geography'],
            'party': item['party'],
            'house': 1,
            'session': spider.session,
            'from': self.from_to['from'],
            'to': self.from_to['to']
        }

        del item['state']
        del item['geography']
        del item['geography_type']
        del item['party']

        return item