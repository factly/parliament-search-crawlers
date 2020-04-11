from scrapy.exceptions import DropItem
import pymongo
import json

class DuplicateCleaner(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        ministries = list(db.ministry.find({}))
       
        self.ministriesSet= set()
        
        for each in ministries:
            self.ministriesSet.add(each['name'].replace(" ", ""))

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
       
        if(item['name'].replace(" ", "") not in self.ministriesSet):
            return item
        else:
            raise DropItem('already_there')

