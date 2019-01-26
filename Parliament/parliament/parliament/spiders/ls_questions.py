# -*- coding: utf-8 -*-
import scrapy
from parliament.items import ParliamentItem
from bs4 import BeautifulSoup
import requests
from scrapy.http import HtmlResponse


class LsQuestionsSpider(scrapy.Spider):
    name = 'ls_questions'
    # allowed_domains = ['http://164.100.47.194']
    start_urls = ['http://164.100.47.194/Loksabha/Questions/Qtextsearch.aspx/']

    def parse(self, response):
        questions = response.css('table.member_list_table > tr')[0:3]
        for question in questions:
            item = ParliamentItem()
            item['question_number'] = question.css("td[style*='width: 5%'] a::text").extract_first()
            item['question_type'] = question.css("td[style*='width: 7%'] a::text")[0].extract().strip()
            item['english_pdf'] = question.css("td[style*='width: 7%'] a[href*='pdf']::attr(href)").extract_first()
            if question.css("td[style*='width: 7%'] a[href*='hindi']::attr(href)").extract_first():
                item['hindi_pdf'] = question.css("td[style*='width: 7%'] a[href*='hindi']::attr(href)").extract_first()
            else:
                item['hindi_pdf'] = ""
            item["date"] = question.css("td[style*='width: 7%']")[1].css("a::text").extract_first()
            item["ministry"] = question.css("td[style*='width: 20%']")[0].css("a::text").extract_first()
            item["members"] = question.css("td[style*='width: 20%']")[1].css("a::text").extract()
            item["subject"] = question.css("td[style*='width: 30%'] a::text").extract_first()
            item["link"] = "http://164.100.47.194/Loksabha/Questions/" + question.css("td[style*='width: 30%'] a::attr(href)").extract()[0]
            item = self.parse_question(item)
            yield item

    def parse_question(self, item):
        request = requests.get(item["link"])
        response = HtmlResponse(url=item["link"], body=request.text, encoding='utf-8')
        item["text"] = BeautifulSoup(response.css("table[style='margin-top: -15px;']").extract_first(), features="lxml").text.strip()
        return item
