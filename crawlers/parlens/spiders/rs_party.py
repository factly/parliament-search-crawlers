# -*- coding: utf-8 -*-
import scrapy


class RSPartySpider(scrapy.Spider):
    name = 'rs_party'
    start_urls = ['https://rajyasabha.nic.in/rsnew/member_site/partymemberlist.aspx']

    custom_settings = { 
        "ITEM_PIPELINES": {
            'parlens.pipelines.parties.NameCleaner': 10,
            'parlens.pipelines.parties.DuplicateCleaner': 20
        }
    }
    
    def parse(self, response):
        parties = response.css("table#ctl00_ContentPlaceHolder1_GridView1").css("tr")

        for party in parties[1:]:
            yield {
                'name': party.css("td")[1].css("a::text").extract_first(),
            }

    
