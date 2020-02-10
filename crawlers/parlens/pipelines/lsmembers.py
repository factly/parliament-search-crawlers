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

class LSMemberUploader(object):
    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        questionDict = list(db.all_members.find({'terms.session': 17 }, {'LSID': 1}))
       
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