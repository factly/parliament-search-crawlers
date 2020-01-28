import datetime
import time

class DOBCleaner(object):
    def process_item(self, item, spider):
        print(spider)
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