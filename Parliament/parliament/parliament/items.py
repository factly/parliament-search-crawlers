# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ParliamentItem(Item):
    # define the fields for your item here like:
    # name = Field()
    lsno = Field()
    question_number = Field()
    question_type = Field()
    qref = Field()
    date = Field()
    ministry = Field()
    members = Field()
    subject = Field()
    link = Field()
    english_pdf = Field()
    hindi_pdf = Field()
    text = Field()
    meta = Field()

class RajyaSabhaItem(Item):
    session = Field()
    question_number = Field()
    question_type = Field()
    date = Field()
    ministry = Field()
    members = Field()
    subject = Field()
    text = Field()
    meta = Field()
    english_doc = Field()
    hindi_doc =Field() 

class MemberofParliament(Item):
    """
    Data structure to define Member of Parliament information
    """
    id = Field()
    name = Field()
    constituency = Field()
    state = Field()
    party = Field()
    dob = Field()
    birth_place = Field()
    marital_status = Field()
    education = Field()
    profession = Field()
    sons = Field()
    daughters = Field()
    url = Field()
    photo = Field()