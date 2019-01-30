# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ParliamentItem(Item):
    # define the fields for your item here like:
    # name = Field()
    question_number = Field()
    question_type = Field()
    date = Field()
    ministry = Field()
    members = Field()
    subject = Field()
    link = Field()
    english_pdf = Field()
    hindi_pdf = Field()
    text = Field()
    meta = Field()
