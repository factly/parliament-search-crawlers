# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import json
import pymongo
from scrapy.utils.response import open_in_browser
# from parliament.items import RajyaSabhaItem
import datetime


class RsQuestionsSpider(scrapy.Spider):
    name = 'rs_questions_archive'
    # allowed_domains = ['164.100.47.4/newrsquestion/Search_QnoWise.aspx']
    start_urls = ['http://164.100.47.4/newrsquestion/Search_QnoWise.aspx']
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongodb_uri"])
    db = client[config["database"]]
    collection = db["rajya_sabha_archive_questions"]
    # collection = db[config["mongo_collection"]["rs"]]
    # db = client["factly_parliament_search"]
    # collection = db["rs_questions"]
    # custom_settings = {"ITEM_PIPELINES": {
    #     'parliament.pipelines.MongoDBPipelineRajyaSabha': 300}
    #     }
    starred = ["STARRED   ","UNSTARRED "]
    current_star_index = 0

    # def parse(self, response):
    #     if self.first_parse:
    #         # self.session_list = response.css("select[name=DRSession] > option::text").extract()[0:1] #Specify the range of sessions here
    #         self.session_list = ["249"]

    def parse(self,response):
        session_list = response.css("select[name=DRSession] > option::text").extract()[3:10]
        # open_in_browser(response)
        for session in session_list:
            form_data = {
                "__EVENTTARGET": "DRSession",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
                "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
                "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
                "q": "",
                "domains": "rajyasabha.nic.in",
                "sitesearch": "rajyasabha.nic.in",
                "DRSession": str(session),
                "TxtQno": "",
                "DRQtype": self.starred[self.current_star_index]
            }

            yield FormRequest (
                url = response.request.url,
                formdata = form_data,
                meta = {
                    "form_data":form_data
                },
            callback = self.iterate_questions
            )


    def iterate_questions(self,response):
        max_questions = int(response.css("span#LabelRange::text").extract_first().strip().split(' ')[4])
        # open_in_browser(response)
        # max_questions = 10
        for question_number in range(1,max_questions+1):
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
                "DRSession": response.meta['form_data']['DRSession'],
                "TxtQno": str(question_number),
                "DRQtype": response.meta['form_data']['DRQtype'],
                "Button2": "Submit"
            }
            carry = {
                "qref": "rs_"+response.meta["form_data"]["DRSession"]+"_"+str(question_number)
            }
            if self.collection.find({"qref": carry["qref"]}).count() > 0:
                continue
            yield FormRequest(
                url = response.request.url,
                formdata = form_data,
                meta = {
                    "form_data" : form_data,
                    "carry" : carry
                },
                callback = self.parse_entry)


    def parse_entry(self,response):
        # open_in_browser(response)
        data_table = response.css("table")[2]
        # open_in_browser(response)
        carry = {}
        carry["date"] = data_table.css("tr")[2].css("td")[3].css("::text").extract()[1]
        carry["qref"] = response.meta["carry"]["qref"]
        carry["ministry"] = data_table.css("tr")[2].css("td")[4].css("::text").extract_first()
        carry["members"] = data_table.css("tr")[2].css("td")[5].css("::text").extract_first().strip()
        carry["subject"] = data_table.css("tr")[2].css("td")[6].css("::text").extract_first()
        print(response.meta["carry"]["qref"])
        form_data = {
            "__EVENTTARGET": "DG1$_ctl3$Hyperlink1",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
            "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
            "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
            "q": "",
            "domains": "rajyasabha.nic.in",
            "sitesearch": "rajyasabha.nic.in",
            "DRSession": response.meta['form_data']['DRSession'],
            "TxtQno": str(response.meta['form_data']['TxtQno']),
            "DRQtype": response.meta['form_data']['DRQtype']
        }

        yield FormRequest(
            url = response.request.url,
            formdata = form_data,
            meta = {
                "form_data" : form_data,
                "carry" : carry
            },
            callback = self.parse_question,
            dont_filter = True
            )

    def parse_question(self,response):
        # print(response.meta["carry"]["qref"])
        # print(response.meta["form_data"])
        # open_in_browser(response)
        item = {}
        item["qref"] = response.meta["carry"]["qref"]
        item["rsno"] = response.meta["form_data"]["DRSession"]
        item["question_number"] = response.meta["form_data"]["TxtQno"]
        item["question_type"] = response.meta["form_data"]["DRQtype"].strip()
        item["date"] = response.meta["carry"]["date"]
        item["ministry"] = response.meta["carry"]["ministry"]
        item["members"] = [response.meta["carry"]["members"]]
        item["subject"] = response.meta["carry"]["subject"]
        item["meta"] = {
            "fetched_on" : str(datetime.datetime.now())
        }
        item["text"] = "\n".join([_.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","") for _ in  response.css("table")[1].css("::text").extract()])
        item["question"] = "\n".join(response.css("span#LabQn").css("::text").extract())
        item["answer"] = "\n".join(response.css("span#LabAns").css("::text").extract())
        self.collection.insert_one(item)



# # -*- coding: utf-8 -*-
# import scrapy
# import json
# import pymongo
# from scrapy.utils.response import open_in_browser
# from parliament.items import RajyaSabhaItem
# import datetime


# class RsQuestionsSpider(scrapy.Spider):
#     name = 'rs_questions'
#     # allowed_domains = ['164.100.47.4/newrsquestion/Search_QnoWise.aspx']
#     start_urls = ['http://164.100.47.4/newrsquestion/Search_QnoWise.aspx']
#     config_file = open("config.json")
#     config = json.load(config_file)
#     client = pymongo.MongoClient(config["mongo_server"])
#     # db = client[config["mongo_database"]]
#     # collection = db[config["mongo_collection"]["rs"]]
#     db = client["factly_parliament_search"]
#     collection = db["rs_questions"]
#     custom_settings = {"ITEM_PIPELINES": {
#         'parliament.pipelines.MongoDBPipelineRajyaSabha': 300}
#         }
#     first_parse = True
#     starred = ["STARRED   ","UNSTARRED "]
#     current_star_index = 0

#     def parse(self, response):
#         if self.first_parse:
#             self.session_list = response.css("select[name=DRSession] > option::text").extract()[0:1] #Specify the range of sessions here
#         for session in self.session_list:
#             form_data = {"__EVENTTARGET": "DRSession",
#                          "__EVENTARGUMENT": "",
#                          "__LASTFOCUS": "",
#                          "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
#                          "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
#                          "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
#                          "q": "",
#                          "domains": "rajyasabha.nic.in",
#                          "sitesearch": "rajyasabha.nic.in",
#                          "DRSession": str(session),
#                          "TxtQno": "",
#                          "DRQtype": "STARRED   "}
#             # print(form_data)
#             yield scrapy.FormRequest(
#                     response.request.url,
#                     formdata=form_data,
#                     meta = {"form_data":form_data},
#                     callback=self.parse_question_list
#                 )
    
#     def parse_question_list(self,response):






#     def parse_max_question(self, response):
#             max_questions = int(response.css("span[id=LabelRange]::text").extract()[0].split('-')[1][:-2].strip())
#             for current_question in range(1,max_questions+1): #Specify the range of questions here
#                 query = {"question_number": response.css("select[name='DRSession'] > option[selected='selected']::text").extract_first()+"_"+str(current_question)}
#                 if self.collection.find(query).count() > 0:
#                     print(query)
#                     continue
#                 form_data = {"__EVENTTARGET": "",
#                              "__EVENTARGUMENT": "",
#                              "__LASTFOCUS": "",
#                              "__VIEWSTATE": response.css("input[name='__VIEWSTATE']::attr(value)").extract_first(),
#                              "__VIEWSTATEGENERATOR": response.css("input[name='__VIEWSTATEGENERATOR']::attr(value)").extract_first(),
#                              "__EVENTVALIDATION": response.css("input[name='__EVENTVALIDATION']::attr(value)").extract_first(),
#                              "q": "",
#                              "domains": "rajyasabha.nic.in",
#                              "sitesearch": "rajyasabha.nic.in",
#                              "DRSession": response.meta['form_data']['DRSession'],
#                              "TxtQno": str(current_question),
#                              "DRQtype": "STARRED   ",
#                              "Button2": "Submit"
#                              }
#                 # print(form_data)
#                 yield scrapy.FormRequest(
#                     response.request.url,
#                     formdata=form_data,
#                     meta = {"form_data":form_data},
#                     callback=self.parse_question_list,
#                     dont_filter = True
#                 )

#     def parse_question_list(self, response):
#         form_data = {
#             "__EVENTTARGET": "DG1$_ctl3$Hyperlink1",
#             "__EVENTARGUMENT": "",
#             "__LASTFOCUS": "",
#             "__VIEWSTATE": response.css("input[name='__VIEWSTATE']::attr(value)").extract_first(),
#             "__VIEWSTATEGENERATOR": response.css("input[name='__VIEWSTATEGENERATOR']::attr(value)").extract_first(),
#             "__EVENTVALIDATION": response.css("input[name='__EVENTVALIDATION']::attr(value)").extract_first(),
#             "q": "",
#             "domains": "rajyasabha.nic.in",
#             "sitesearch": "rajyasabha.nic.in",
#             "DRSession": response.meta['form_data']['DRSession'],
#             "TxtQno": str(response.meta['form_data']['TxtQno']),
#             "DRQtype": "STARRED   "
#         }
#         # print(form_data)
#         yield scrapy.FormRequest(
#                 response.request.url,
#                 formdata=form_data,
#                 meta = {"form_data":form_data},
#                 callback=self.parse_question,
#                 dont_filter = True
#             )
    
#     def parse_question(self,response):
#         # open_in_browser(response)
#         # item = RajyaSabhaItem()
#         item = {}
#         item['session'] = response.meta['form_data']['DRSession']
#         item['question_number'] = item['session']+"_"+str(response.css("span#Label3::text").extract_first())
#         item['question_type'] = self.starred[self.current_star_index].rstrip()
#         item['date'] = response.css("span#Label6::text").extract_first()
#         item['ministry'] = response.css("span#Label1::text").extract_first()
#         item['subject'] = response.css("font[color=Blue]::text").extract_first()
#         item['members'] = response.css("span#LabMp::text").extract()
#         item['text'] = '\n'.join([x.rstrip() for x in response.css('table#Table2 *::text').extract()])
#         item['meta'] = {"fetched_on":str(datetime.datetime.now())}
#         item['question'] = response.css("span#LabQn::text").extract
#         item['answer'] = response.css("span#LabAns")
#         item['english_doc'] = response.css("a[href*='annex']::attr(href)").extract_first()
#         item['hindi_doc'] = response.css("a[href*='qhindi']::attr(href)").extract_first()
#         # json.dump(dict(item),open("rj.json","w"))
#         yield item