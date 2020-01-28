# -*- coding: utf-8 -*-
import scrapy


class LSPartySpider(scrapy.Spider):
    name = 'ls_party'
    start_urls = ['http://loksabhaph.nic.in/Members/PartywiseList.aspx']

    def parse(self, response):
        parties = response.css("table.member_list_table").css("tr")
        for party in parties[1:]:
            yield {
                'name': party.css("td")[1].css("a::text").extract_first()
            }
