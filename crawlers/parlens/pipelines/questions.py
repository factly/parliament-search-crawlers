import pymongo
import json

# based on ministries.json change ministry name to MID 
class MinistryMatching(object):
    def open_spider(self, spider):    
        with open('./data/ministries.json', 'r', encoding='utf-8') as f:
            self.ministries = json.load(f)

    def process_item(self, item, spider):
        if item['ministry'].strip().upper() in self.ministries:
            item['ministry'] = self.ministries[item['ministry'].strip().upper()]   
        else:
            missing_message = {
                'qref': item['qref'],
                'item': item['ministry'],
                'message': "ministry not found"
            }
            spider.error.write(json.dumps(missing_message) + "\n")
        return item
        
# final check for question
class QuestionFinal(object):

    def process_item(self, item, spider):
        dateRow = item['date'].split(".")
        houseMapper = {
            'Lok Sabha': 1,
            'Rajya Sabha': 2
        }
        item['date'] = dateRow[2] + "-" + dateRow[1] + "-" + dateRow[0]
        item['house'] = houseMapper[item['house']]

        return item
