from scrapy.exceptions import DropItem
import pymongo
import json

class NameCleaner(object):
    def process_item(self, item, spider):
        nameRaw = item['name']
        nameList = nameRaw.split("(")
        if len(nameList) == 2:
            name = nameList[0]
            abbr = nameList[1][:-1]
        elif len(nameList) == 4:
            name = nameList[0].strip() + " (" + nameList[1].strip()
            abbr = nameList[2].strip() + " (" + nameList[3][:-1]

        item['name'] = " ".join(name.split())
        item['abbr'] = abbr.replace(" ", "").upper()

        return item


class DuplicateCleaner(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        parties = list(db.all_parties.find({}))
       
        self.partiesSet = set()
        
        for each in parties:
            self.partiesSet.add(each['name'].lower())

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
       
        if(item['name'].lower() not in self.partiesSet):
            return item
        else:
            raise DropItem('already_there')

