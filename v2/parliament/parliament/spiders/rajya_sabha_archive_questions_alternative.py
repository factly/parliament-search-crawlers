# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import json
import pymongo
from scrapy.utils.response import open_in_browser
# from parliament.items import RajyaSabhaItem
import datetime


class RsQuestionsSpider(scrapy.Spider):
    name = 'rs_questions_archive_alternative'
    # allowed_domains = ['164.100.47.4/newrsquestion/Search_QnoWise.aspx']
    start_urls = ['https://rajyasabha.nic.in/rsnew/Questions/Search_QnoWise.aspx']
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongodb_uri"])
    db = client[config["database"]]
    collection = db["rajya_sabha_archive_questions"]
    # collection = db[config["mongo_collection"]["rs"]]
    # db = client["factly_parliament_search"]
    # collection = db["rs_questions"]
    # custom_settings = {
    #     'USER_AGENT': 'Factly Parliament Search Bot',
    #     }
    starred = ["STARRED   ","UNSTARRED "]
    current_star_index = 1
    error_file = open("errors4.log","a+")

    # def parse(self, response):
    #     if self.first_parse:
    #         # self.session_list = response.css("select[name=DRSession] > option::text").extract()[0:1] #Specify the range of sessions here
    #         self.session_list = ["249"]

    def parse(self,response):
        self.error_file.write("\n\n\n######## Rajya Sabha Archive Crawler "+str(datetime.datetime.now())+" ###########\n" )
        # session_list = response.css("select#ctl00_ContentPlaceHolder1_DRSession").css("option::attr(value)").extract()
        session_list = [247]
        # open_in_browser(response)
        for session in session_list:
            form_data = {
                "__EVENTTARGET": "ctl00$ContentPlaceHolder1$DRSession",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
                "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
                "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
                "q": "",
                "domains": "rajyasabha.nic.in",
                "sitesearch": "rajyasabha.nic.in",
                "ctl00$ContentPlaceHolder1$DRSession": str(session),
                "ctl00$ContentPlaceHolder1$TxtQno": "",
                "ctl00$ContentPlaceHolder1$DRQtype": self.starred[self.current_star_index]
            }

            yield FormRequest (
                url = response.request.url,
                formdata = form_data,
                meta = {
                    "form_data":form_data,
                    "caller" : "parse",
                    "qref" : "rs_"+str(session)
                },
            callback = self.iterate_questions,
            errback = self.error_handler
            )


    def iterate_questions(self,response):
        max_questions = int(response.css("span#ctl00_ContentPlaceHolder1_LabelRange::text").extract_first().strip().split(" ")[4])
        # open_in_browser(response)
        # max_questions = 1
        for question_number in range(1,max_questions+1):
        # for question_number in range(2,3):
            form_data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
                "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
                "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
                "q": "",
                "domains": "rajyasabha.nic.in",
                "sitesearch": "rajyasabha.nic.in",
                "ctl00$ContentPlaceHolder1$DRSession": response.meta['form_data']['ctl00$ContentPlaceHolder1$DRSession'],
                "ctl00$ContentPlaceHolder1$TxtQno": str(question_number),
                "ctl00$ContentPlaceHolder1$DRQtype": response.meta['form_data']['ctl00$ContentPlaceHolder1$DRQtype'],
                "ctl00$ContentPlaceHolder1$Button2": "Submit"
            }
            carry = {
                "qref": "rs_"+response.meta["form_data"]["ctl00$ContentPlaceHolder1$DRSession"]+"_"+str(question_number)+"_"+response.meta["form_data"]["ctl00$ContentPlaceHolder1$DRQtype"].strip()
            }
            # if self.collection.find({"qref": carry["qref"]}).count() > 0:
            #     print(carry["qref"])
            #     continue
            yield FormRequest(
                url = response.request.url,
                formdata = form_data,
                meta = {
                    "form_data" : form_data,
                    "carry" : carry,
                    "caller" : "iterate_questions",
                    "qref" : carry["qref"]
                },
                callback = self.parse_entry,
                errback = self.error_handler)


    def parse_entry(self,response):
        open_in_browser(response)
        data_table = response.css("table#ctl00_ContentPlaceHolder1_DG1")
        carry = {}
        if(len(data_table.css("tr")) >= 2):
            carry["date"] = data_table.css("tr")[2].css("td")[3].css("::text").extract()[1]
            carry["qref"] = response.meta["carry"]["qref"]
            carry["ministry"] = data_table.css("tr")[2].css("td")[4].css("::text").extract_first()
            carry["members"] = data_table.css("tr")[2].css("td")[5].css("::text").extract_first().strip()
            carry["subject"] = data_table.css("tr")[2].css("td")[6].css("::text").extract_first()
            print(response.meta["carry"]["qref"])
        else:
            carry["date"]  = ""
            carry["qref"]  = response.meta["carry"]["qref"]
            carry["ministry"]  = ""
            carry["members"]  = ""
            carry["subject"]  = ""
            self.error_file.write(carry["qref"]+" list error\n")
        form_data = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$DG1$ctl03$Hyperlink1",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
            "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
            "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
            "q": "",
            "domains": "rajyasabha.nic.in",
            "sitesearch": "rajyasabha.nic.in",
            "ctl00$ContentPlaceHolder1$DRSession": response.meta['form_data']['ctl00$ContentPlaceHolder1$DRSession'],
            "ctl00$ContentPlaceHolder1$TxtQno": str(response.meta['form_data']['ctl00$ContentPlaceHolder1$TxtQno']),
            "ctl00$ContentPlaceHolder1$DRQtype": response.meta['form_data']['ctl00$ContentPlaceHolder1$DRQtype']
        }

        yield FormRequest(
            url = response.request.url,
            formdata = form_data,
            meta = {
                "form_data" : form_data,
                "carry" : carry,
                "caller" : "parse_entry",
                "qref" : carry["qref"]
            },
            callback = self.parse_question,
            dont_filter = True,
            errback = self.error_handler
            )

    def parse_question(self,response):
        # print(response.meta["carry"]["qref"])
        # print(response.meta["form_data"])
        # open_in_browser(response)
        item = {}
        item["qref"] = response.meta["carry"]["qref"]
        print("Parsing: ",item["qref"])
        item["rsno"] = response.meta["form_data"]["ctl00$ContentPlaceHolder1$DRSession"]
        item["question_number"] = response.meta["form_data"]["ctl00$ContentPlaceHolder1$TxtQno"]
        item["question_type"] = response.meta["form_data"]["ctl00$ContentPlaceHolder1$DRQtype"].strip()
        item["date"] = response.meta["carry"]["date"]
        item["ministry"] = response.meta["carry"]["ministry"]
        item["members"] = [response.meta["carry"]["members"]]
        item["subject"] = response.meta["carry"]["subject"]
        item["meta"] = {
            "fetched_on" : str(datetime.datetime.now())
        }
        item["text"] = "\n".join([_.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","") for _ in  response.css("table")[1].css("::text").extract()])
        item["question"] = "\n".join(response.css("span#ctl00_ContentPlaceHolder1_LabQn").css("::text").extract())
        item["answer"] = "\n".join(response.css("span#ctl00_ContentPlaceHolder1_LabAns").css("::text").extract())
        self.collection.insert_one(item)

    def error_handler(self,failure):
        error_message = {
            "qref" : failure.reques.meta["qref"],
            "caller" : failure.request.meta["caller"]
        }
        self.error_file.write(json.dumps(error_message))
