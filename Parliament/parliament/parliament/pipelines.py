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
        config_file = open('config.json')
        config = json.load(config_file)
        client = pymongo.MongoClient(config["mongo_server"])
        db = client[config["mongo_database"]]
        self.collection = db[config["mongo_collection"]]

    def process_item(self, item, spider):
        if self.collection.find({"qref": item["qref"]}).count() > 0:
            logging.debug("Question already exists in database!")
            return item
        else:
            self.collection.insert(dict(item))
            logging.debug("Question added to MongoDB database!")
            return item