# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParlensItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Questions(scrapy.Item):
    qref = scrapy.Field()
    house = scrapy.Field()
    ministry = scrapy.Field()
    date = scrapy.Field()
    subject = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    questionBy = scrapy.Field()
    englishPdf = scrapy.Field()
    hindiPdf = scrapy.Field()
    type = scrapy.Field()

class LSMembers(scrapy.Item):
    LSID = scrapy.Field()
    name = scrapy.Field()
    prefix = scrapy.Field()
    memberName = scrapy.Field()
    geography = scrapy.Field()
    state = scrapy.Field()
    geography_type = scrapy.Field()
    party = scrapy.Field()
    dob = scrapy.Field()
    birth_place = scrapy.Field()
    marital_status = scrapy.Field()
    sons = scrapy.Field()
    daughters = scrapy.Field()
    education = scrapy.Field()
    profession = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    term = scrapy.Field()

class RSMembers(scrapy.Item):
    RSID = scrapy.Field()
    name = scrapy.Field()
    prefix = scrapy.Field()
    memberName = scrapy.Field()
    geography = scrapy.Field()
    party = scrapy.Field()
    dob = scrapy.Field()
    birth_place = scrapy.Field()
    marital_status = scrapy.Field()
    children = scrapy.Field()
    sons = scrapy.Field()
    daughters = scrapy.Field()
    education = scrapy.Field()
    profession = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    term = scrapy.Field()