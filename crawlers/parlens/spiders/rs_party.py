# -*- coding: utf-8 -*-
import scrapy


class RSPartySpider(scrapy.Spider):
    name = 'rs_party'
    start_urls = ['https://rajyasabha.nic.in/rsnew/member_site/partymemberlist.aspx']

    def parse(self, response):
        parties = response.css("table#ctl00_ContentPlaceHolder1_GridView1").css("tr")

        for party in parties[1:]:
            yield {
                'name': " ".join(party.css("td")[1].css("a::text").extract_first().split()),
            }

    
