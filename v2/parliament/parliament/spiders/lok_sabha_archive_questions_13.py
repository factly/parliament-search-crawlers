# -*- coding: utf-8 -*-
import scrapy
# from parliament.items import ParliamentItem
from bs4 import BeautifulSoup
import requests
from scrapy.http import HtmlResponse, Request
import datetime
import json
import re
import pymongo
import os
'''To invoke this spider type "scrapy crawl ls_questions" in terminal with parliament-search-crawlers/Parliament/parliament
as the active directory'''


class LsQuestionsSpider(scrapy.Spider):
    print(os.listdir())
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongodb_uri"])
    db = client[config["database"]]
    collection = db["lok_sabha_archive_questions"]
    name = 'ls_archive_questions_13'
    meta = {}
    page_flag = False
    current_ls = "13"
    detected = open("logs/detected_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".log","w+")
    skipped = open("logs/skipped_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S") +".log","w+")
    written = open("logs/written_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S") +".log","w+")
    errors = open("logs/errors_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S") +".log","w+")
    start_urls = ['http://loksabhaph.nic.in/Questions/qsearch15.aspx?lsno='+current_ls]

    # Use the following two lines to run the crawler from a specific page
    current_page = 7009
    meta["current_page"] = current_page
    page_flag = True

    # This will act as the entry point of the spider
    def parse(self, response):
        if response.status == 404:
            self.errors.write(response.request.url+"\n")
            yield scrapy.Request(response.request.url)
        else:
            # Default value for submission to aspx form
            form_data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                "__VIEWSTATEGENERATOR": response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                "__VIEWSTATEENCRYPTED": "",
                "__EVENTVALIDATION": response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                "ctl00$txtSearchGlobal": "",
                "ctl00$ContentPlaceHolder1$ddlfile": ".pdf",
                "ctl00$ContentPlaceHolder1$TextBox1": "",
                "ctl00$ContentPlaceHolder1$btn": "allwordbtn",
                "ctl00$ContentPlaceHolder1$btn1": "titlebtn",
                "ctl00$ContentPlaceHolder1$txtpage": 1,
                "ctl00$ContentPlaceHolder1$btngo": "Go"
            }

            print(self.current_page)
            # Some metadata for debugging purpose
            self.meta["total_pages"] = int(
                response.css("span#ContentPlaceHolder1_lblfrom::text").extract_first().strip().split(' ')[1])
            # Limit the number of pages to test the script
            # self.meta["total_pages"] = 1
            if not self.page_flag:
                self.meta["current_page"] = int(response.css("input#ContentPlaceHolder1_txtpage::attr(value)").extract_first())
            else:
                self.page_flag = False
            self.meta["page_url"] = response.request.url

            # Select all questions from the page (currently 10 per page)
            questions = response.css('table.member_list_table > tr')
            for question in questions:
                # Writing details of each question to a ParliamentItem object (see items.py for more details)
                item = {}
                item['lsno'] = int(self.current_ls)
                item['link'] = "http://loksabhaph.nic.in/Questions/" + question.css("td[style*='width: 30%'] a::attr(href)").extract()[0]
                item['qref'] = re.search("qref=[0-9]+",item['link']).group().split("=")[1]
                self.detected.write(item['link']+"\n")
                if self.collection.find({"link": item["link"]}).count() > 0:
                    self.skipped.write(item['link']+"\n")
                    continue
                self.meta["fetched_on"] = str(datetime.datetime.now())
                item['question_number'] = question.css("td[style*='width: 5%'] a::text").extract_first()
                item['question_type'] = question.css("td[style*='width: 7%'] a::text")[0].extract().strip()
                if question.css("td[style*='width: 7%'] a[href*='pdf']::attr(href)").extract_first():
                    item['english_pdf'] = question.css("td[style*='width: 7%'] a[href*='pdf']::attr(href)").extract_first()
                else:
                    item['english_pdf'] = ""
                if question.css("td[style*='width: 7%'] a[href*='hindi']::attr(href)").extract_first():
                    item['hindi_pdf'] = question.css("td[style*='width: 7%'] a[href*='hindi']::attr(href)").extract_first()
                else:
                    item['hindi_pdf'] = ""
                item['date'] = question.css("td[style*='width: 7%']")[1].css("a::text").extract_first()
                item['ministry'] = question.css("td[style*='width: 20%']")[0].css("a::text").extract_first()
                item['members'] = question.css("td[style*='width: 20%']")[1].css("a::text").extract()
                item['subject'] = question.css("td[style*='width: 30%'] a::text").extract_first()
                item['meta'] = self.meta
                # print(item)
                # item = self.parse_question(item)
                # self.data.append(dict(item))
                # json.dump(self.data,open("questions.json","w"))
                yield Request(url=item['link'], meta={"item":item}, callback=self.parse_question)

            # If this is not the last page go to the next page
            # if self.meta["current_page"] < self.meta["total_pages"]:
            if self.meta["current_page"] > 1:
                self.current_page -= 1
                form_data['ctl00$ContentPlaceHolder1$txtpage'] = str(self.current_page)#str(self.meta["current_page"] + 1)
                yield scrapy.FormRequest(
                    self.meta["page_url"],
                    formdata=form_data,
                    callback=self.parse,
                )

    # Fetch the question from the link and persist to MongoDB
    def parse_question(self, response):
        item = response.meta["item"]
        item["text"] = BeautifulSoup(response.css("table[style='margin-top: -15px;']").extract_first(),
            features="lxml").text.strip()
        item["question"] = "\n".join(response.css("table[style='margin-top: -15px;']").css("td.stylefontsize")[0].css("::text").extract()).strip()
        item["answer"] = "\n".join(response.css("table[style='margin-top: -15px;']").css("td.stylefontsize")[1].css("::text").extract()).strip()
        # print(item)
        result = self.collection.insert_one(item)
        ins_flag = False
        if self.collection.count_documents({"qref":item["qref"]}) == 1:
            self.written.write(item['link']+"\n")
            ins_flag = True
        else:
            self.errors.write(item['link']+"\n")
