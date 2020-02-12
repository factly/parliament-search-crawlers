from scrapy.exceptions import DropItem
import pymongo
import json

class DuplicateCleaner(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        ministries = list(db.ministry.find({}))
       
        self.ministriesDict = dict()
        
        for each in ministries:
            self.ministriesDict[each['name']] = each['MINID']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
       
        if(item['name'] not in self.ministriesDict):
            return item
        else:
            raise DropItem('already_there')

