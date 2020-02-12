# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import FormRequest
from parlens.items import Questions
import json
import datetime


class LSQuestionsSpider(scrapy.Spider):
    name = 'ministries'

    custom_settings = { 
        "ITEM_PIPELINES": {
            'parlens.pipelines.ministries.DuplicateCleaner': 5
        }
    }

    def __init__(self, session='', **kwargs):
        super().__init__(**kwargs) 
        if(session):
            self.session = str(session)
        else:
            raise scrapy.exceptions.CloseSpider('session_not_found')

        self.start_urls = ["http://loksabhaph.nic.in/Questions/qsearch15.aspx?lsno="+session]

        self.error = open("./logs/errors.log","a+")
        self.error.write("\n\n\n######## Lok Sabha Question Crawler "+str(datetime.datetime.now())+" ###########\n" )
    
    def parse(self,response):
        ministries = response.css("select#ContentPlaceHolder1_ddlministry").css("option")
        
        for ministry in ministries[1:]:
            name = ministry.css("::text").extract_first()
            LSID = ministry.css("::attr(value)").get()
            yield {
                'LSID': int(LSID),
                'name': name.strip()
            }