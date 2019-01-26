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
import os


class MongoDBPipeline(object):
    def __init__(self):
        # connection = pymongo.MongoClient(settings['MONGODB_SERVER'])
        # db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]
        print(os.listdir(os.getcwd()))
        config_file = open('config.json')
        config = json.load(config_file)
        client = pymongo.MongoClient(config["mongo_server"])
        db = client[config["mongo_database"]]
        self.collection = db[config["mongo_collection"]]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.debug("Question added to MongoDB database!")
        return item

# class ParliamentPipeline(object):
#     def process_item(self, item, spider):
#         return item
