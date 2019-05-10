# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

# from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
import json
# import os


class MongoDBPipelineLokSabha(object):
    # def __init__(self):
        # config_file = open('config.json')
        # config = json.load(config_file)
        # client = pymongo.MongoClient(config["mongo_server"])
        # db = client[config["mongo_database"]]
        # self.collection = db[config["mongo_collection"]]
    def process_item(self, item, spider):
        logging.debug("Lok Sabha")
        collection = spider.collection
        if collection.find({"qref": item["qref"]}).count() > 0:
            logging.debug("Question already exists in database!")
            return item
        else:
            collection.insert(dict(item))
            logging.debug("Question added to MongoDB database!")
            return item

class MongoDBPipelineRajyaSabha(object):
    # def __init__(self):
        # self.data = json.load(open("rj.json","r"))
        # self.data_file = open("rj.json","w")
    def process_item(self, item, spider):
        logging.debug("Rajya Sabha")
        collection = spider.collection
        # logging.debug(collection.full_name)
        query = {"text": item["text"]}
        logging.debug(query)
        if collection.find(query).count() > 0:
            logging.debug("Question already exists in database!")
            return item
        else:
            collection.insert(dict(item))
            # self.data.append(dict(item))
            # json.dump(self.data,self.data_file)
            logging.debug("Question added to MongoDB database!")
            return item

class MembersPipeline(object):

    def process_item(self,item,spider):
        collection = spider.collection
        # logging.debug("Member")
        query = {"id": item["id"]}
        if collection.find(query).count() > 0:
            logging.debug("Member already exists in database!")
            return item
        else:
            collection.insert(dict(item))
            # self.data.append(dict(item))
            # json.dump(self.data,self.data_file)
            logging.debug("Member added to MongoDB database!")
            return item
        # data = json.load(open("members.json","r"))
        # data.append(dict(item))
        # json.dump(data,open("members.json","w"))