from scrapy.exceptions import DropItem
import pymongo
import json

# remove already existing question based on qref (session_questionID)
class DuplicateCleaner(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))

        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        questionDict = list(db.questions.find(
            {'qref': {'$regex': spider.session + "_",  '$options': 'i'}}, {'qref': 1}))

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


class QuestionByCleaning(object):
    def process_item(self, item, spider):
        newQuestionBy = list()
        for asker in item['questionBy']:
            askerNew = asker.replace(",", " ").strip()
            askerNew = " ".join(askerNew.split()).strip()
            if(askerNew in spider.NameToLSID):
                newQuestionBy.append(int(spider.NameToLSID[askerNew]))
            else:
                missing_message = {
                    'qref': item['qref'],
                    'item': askerNew,
                    'message': "Name not found in NameToMID"
                }
                spider.error.write(json.dumps(missing_message) + "\n")

        item['questionBy'] = newQuestionBy

        return item
# match questionBy name with db name
class QuestionByMatching(object):

    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))

        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        members = list(db.members.find(
            {'terms.house': 1, 'terms.session': int(spider.session)}, {'MID': 1, 'LSID': 1}))

        self.LSIDtoMID = dict()

        for member in members:
            self.LSIDtoMID[member['LSID']] = member['MID']
    
        spider.error.write(json.dumps(self.LSIDtoMID) + "\n")

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
                    'extra': item['questionBy'],
                    'message': "LSID not found in LSIDtoMID"
                }
                spider.error.write(json.dumps(missing_message) + "\n")

        item['questionBy'] = questionByIDs
        return item
