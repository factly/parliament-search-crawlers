# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from parlens.items import Questions
import json
import datetime


class RSQuestionsSpider(scrapy.Spider):
    name = 'rs_questions'

    def __init__(self, session='', qtype='', **kwargs):
        super().__init__(**kwargs) 
  
        if(session):
            self.session = str(session)
        else:
            raise scrapy.exceptions.CloseSpider('session_not_found')

        if(qtype):
            qTypeList = ["STARRED   ", "UNSTARRED "]
            self.questionType = str(qTypeList[int(qtype)])
        else:
            raise scrapy.exceptions.CloseSpider('type_not_found')
    
        with open( "./data/rsqno.json", 'r', encoding='utf-8') as f:
            qnos = json.load(f)
        
        if(self.session in qnos):
            self.max_questions = qnos[self.session][self.questionType.strip()]
        else:
            raise scrapy.exceptions.CloseSpider('bandwidth_exceeded')

        self.error = open("./logs/errors.log","a+")
        self.error.write("\n\n\n######## Rajya Sabha Question Crawler "+str(datetime.datetime.now())+" ###########\n" )
        
    start_urls = ['https://rajyasabha.nic.in/rsnew/Questions/Search_QnoWise.aspx']

    custom_settings = { 
        "ITEM_PIPELINES": {
            'parlens.pipelines.questions.MinistryMatching': 10, 
            'parlens.pipelines.questions.RSAskedByCleaning': 20,
            'parlens.pipelines.questions.QuestionByMatching': 30,
            'parlens.pipelines.questions.QuestionFinal': 40,
            'parlens.pipelines.rsquestions.RSQuestionUploader': 50
        }
    }

    
    def parse(self,response):
        for question_number in range(1, self.max_questions + 1):
 
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
                "ctl00$ContentPlaceHolder1$DRSession": self.session,
                "ctl00$ContentPlaceHolder1$TxtQno": str(question_number),
                "ctl00$ContentPlaceHolder1$DRQtype": self.questionType,
                "ctl00$ContentPlaceHolder1$Button2": "Submit"
            }

            yield FormRequest(
                url = response.request.url,
                formdata = form_data,
                callback = self.parse_entry,
                errback = self.error_handler,
                meta={
                    'session': self.session,
                    'type': self.questionType,
                    'qno': str(question_number)
                }
            )


    def parse_entry(self,response):
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
            "ctl00$ContentPlaceHolder1$DRSession": response.meta['session'],
            "ctl00$ContentPlaceHolder1$TxtQno": response.meta['qno'],
            "ctl00$ContentPlaceHolder1$DRQtype": response.meta['type']
        }

        yield FormRequest(
            url = response.request.url,
            formdata = form_data,
            meta = response.meta,
            callback = self.parse_question,
            dont_filter = True,
            errback = self.error_handler
        )

    def parse_question(self,response):
        try:

            linkTable = response.css("table#Table3")

            yield Questions(
                qref = response.meta['session'] + '_' + response.meta['type'].strip() + '_' + response.meta['qno'],
                house = "Rajya Sabha",
                ministry = str(response.css("span#ctl00_ContentPlaceHolder1_Label1").css("::text").extract_first()),
                date = str(response.css("span#ctl00_ContentPlaceHolder1_Label6").css("::text").extract_first()),
                subject = str(response.css("span#ctl00_ContentPlaceHolder1_LabTitle").css("::text").extract_first()),
                question = response.css("span#ctl00_ContentPlaceHolder1_LabQn").get(),
                answer = response.css("span#ctl00_ContentPlaceHolder1_LabAns").get(),
                questionBy = response.css("span#ctl00_ContentPlaceHolder1_LabMp").css("::text").extract(),
                englishPdf = linkTable.css("tr")[0].css("td")[0].css("a")[1].css("a::attr(href)").extract_first(),
                hindiPdf = linkTable.css("tr")[0].css("td")[0].css("a")[3].css("a::attr(href)").extract_first(),
                type = response.meta['type'].strip()
            )
            
        except:
            error_message = {
                "type": "ERROR",
                "qref" : response.meta['session'] + '_' + response.meta['type'].strip() + '_' + response.meta['qno']
            }
            self.error.write(json.dumps(error_message) + "\n")

    def error_handler(self,failure):
        error_message = {
            "type": "ERROR",
            "qref" : response.meta['session'] + '_' + response.meta['type'].strip() + '_' + response.meta['qno']
        }
        self.error.write(json.dumps(error_message) + "\n")
