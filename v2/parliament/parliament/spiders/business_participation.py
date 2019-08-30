# -*- coding: utf-8 -*-
import scrapy
import os
import json

class BusinessParticipationSpider(scrapy.Spider):
    name = 'business_participation_17'
    allowed_domains = ['loksabhaph.nic.in/Members/MemberReport16.aspx']
    start_urls = ['http://loksabhaph.nic.in/Members/MemberReport16.aspx/']
    config = json.load(open("./config.cfg"))
    def start_requests(self, response):
        root_directory = "../Downloaded_Pages/Business_Participation_16/"
        downloaded_pages = os.listdir(root_directory)

        # for page in downloaded_pages:
            
    def parse(self, response):
        pass
