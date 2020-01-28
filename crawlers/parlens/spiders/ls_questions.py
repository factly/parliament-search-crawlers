# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import FormRequest
from parlens.items import Questions
import json
import datetime


class LSQuestionsSpider(scrapy.Spider):
    name = 'ls_questions'

    def __init__(self, session='', **kwargs):
        super().__init__(**kwargs) 
        if(session):
            self.session = str(session)
        else:
            raise scrapy.exceptions.CloseSpider('session_not_found')

        self.error_file = open("errors.log","a+")
        self.start_urls = ["http://loksabhaph.nic.in/Questions/qsearch15.aspx?lsno="+session]

    custom_settings = { 
        "ITEM_PIPELINES": {
            'parlens.pipelines.questions.MinistryMatching': 10, 
            'parlens.pipelines.questions.LSAskedByMatching': 20,
            'parlens.pipelines.questions.QuestionFinal': 30
        }
    }
    
    def parse(self,response):
        totolPages = str(response.css("span#ContentPlaceHolder1_lblfrom").css("::text").extract_first()).split(" ")
        maxPages = int(totolPages[2])
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
            "ctl00$ContentPlaceHolder1$btngo": "Go"
        }

        for page_number in range(1, maxPages+1):
            form_data['ctl00$ContentPlaceHolder1$txtpage'] = str(page_number) 
            yield FormRequest(
                url = response.request.url,
                formdata = form_data,
                meta = {
                    'session': self.session
                },
                callback = self.parse_questions_page,
                errback = self.error_handler,
            )

    def parse_questions_page(self, response):
        products = response.css("table.member_list_table").css("tr")
        for each in products[1:]:
            QuestionLink = each.css("td")[0].css("a::attr(href)").extract()[0].split("?")[1]
            qref = QuestionLink.split("&")[0].split("=")[1]
            yield Request(
                url = "http://loksabhaph.nic.in/Questions/QResult15.aspx?qref="+str(qref)+"&lsno="+response.meta['session'],
                callback = self.parse_question,
                errback = self.error_handler,
                meta = {
                    'session': response.meta['session'],
                    'qno': str(qref)
                }
            )

    def parse_question(self,response):
        try:
            askedBy = list()
            askedBy.append(str(response.css("span#ContentPlaceHolder1_Label7").css("::text").extract_first()))
            subAskedBy = response.css('table#ContentPlaceHolder1_GridView1').css("td.stylefontsize").css("::text").extract()
            
            for each in subAskedBy:
                askedBy.append(each.replace("\r\n", "").strip())

            item = Questions(
                qref = response.meta['session'] + '_' + response.meta['qno'],
                house = "Lok Sabha",
                ministry = str(response.css("span#ContentPlaceHolder1_Label1").css("::text").extract_first()).strip(),
                date = str(response.css("span#ContentPlaceHolder1_Label4").css("::text").extract_first()),
                subject = str(response.css("span#ContentPlaceHolder1_Label5").css("::text").extract_first()).strip(),
                question = response.css("table[style='margin-top: -15px;']").css("td.stylefontsize")[0].get(),
                answer = response.css("table[style='margin-top: -15px;']").css("td.stylefontsize")[1].get(),
                questionBy = askedBy,
                hindiPdf = response.css("a#ContentPlaceHolder1_HyperLink2").css("::attr(href)").extract_first(),
                englishPdf = response.css("a#ContentPlaceHolder1_HyperLink1").css("::attr(href)").extract_first(),
                type = str(response.css("span#ContentPlaceHolder1_Label2").css("::text").extract_first()).strip()
            )
            yield item

        except:
            error_message = {
                "qref" : response.meta['session'] + '_' + response.meta['qno'],
                "message": 'something went wrong'
            }
            self.error_file.write(json.dumps(error_message) + "\n")
    
    def error_handler(self,failure):
        error_message = {
            "qref" : failure,
            "message": "Error_handler"
        }
        self.error_file.write(json.dumps(error_message) + "\n")
