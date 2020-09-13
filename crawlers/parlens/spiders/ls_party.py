# -*- coding: utf-8 -*-
import scrapy

class LSPartySpider(scrapy.Spider):
    name = 'ls_party'
    start_urls = ['http://loksabhaph.nic.in/Members/PartywiseList.aspx']

    custom_settings = { 
        "ITEM_PIPELINES": {
            'parlens.pipelines.parties.NameCleaner': 10, # remove abbr from name string
            'parlens.pipelines.parties.DuplicateCleaner': 20 # remove already existig party
        }
    }

    def parse(self, response):
        parties = response.css("table.member_list_table").css("tr")
        for party in parties[1:]:
            yield {
                'name': party.css("td")[1].css("a::text").extract_first()
            }
