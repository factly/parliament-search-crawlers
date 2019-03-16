# -*- coding: utf-8 -*-
import scrapy
import json
import pymongo
from scrapy.utils.response import open_in_browser
from parliament.items import RajyaSabhaItem
import datetime


class RsQuestionsSpider(scrapy.Spider):
    name = 'rs_questions'
    # allowed_domains = ['164.100.47.4/newrsquestion/Search_QnoWise.aspx']
    start_urls = ['http://164.100.47.4/newrsquestion/Search_QnoWise.aspx']
    config_file = open("config.json")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongo_server"])
    db = client[config["mongo_database"]]
    collection = db[config["mongo_collection"]["rs"]]
    custom_settings = {"ITEM_PIPELINES": {
        'parliament.pipelines.MongoDBPipelineRajyaSabha': 300}
        }
    first_parse = True
    starred = ["STARRED   ","UNSTARRED "]
    current_star_index = 0

    def parse(self, response):
        if self.first_parse:
            self.session_list = response.css("select[name=DRSession] > option::text").extract() #Specify the range of sessions here
        for session in self.session_list:
            form_data = {"__EVENTTARGET": "DRSession",
                         "__EVENTARGUMENT": "",
                         "__LASTFOCUS": "",
                         "__VIEWSTATE": "/wEPDwUKLTQxMjkyMjY5NQ9kFgICAQ9kFgoCAw8QDxYEHg1EYXRhVGV4dEZpZWxkBQZzZXNfbm8eC18hRGF0YUJvdW5kZ2QQFUUDMjQ4AzI0NwMyNDYDMjQ1AzI0NAMyNDMDMjQyAzI0MQMyNDADMjM5AzIzOAMyMzcDMjM2AzIzNQMyMzQDMjMzAzIzMgMyMzADMjI5AzIyOAMyMjcDMjI2AzIyNQMyMjQDMjIzAzIyMgMyMjEDMjIwAzIxOQMyMTgDMjE3AzIxNQMyMTQDMjEzAzIxMgMyMTEDMjEwAzIwOQMyMDgDMjA3AzIwNgMyMDUDMjA0AzIwMwMyMDIDMjAwAzE5OQMxOTgDMTk3AzE5NgMxOTUDMTk0AzE5MwMxOTIDMTkxAzE5MAMxODkDMTg4AzE4NgMxODUDMTg0AzE4MgMxODEDMTgwAzE3OQMxNzgDMTc2AzE3NQMxNzQVRQMyNDgDMjQ3AzI0NgMyNDUDMjQ0AzI0MwMyNDIDMjQxAzI0MAMyMzkDMjM4AzIzNwMyMzYDMjM1AzIzNAMyMzMDMjMyAzIzMAMyMjkDMjI4AzIyNwMyMjYDMjI1AzIyNAMyMjMDMjIyAzIyMQMyMjADMjE5AzIxOAMyMTcDMjE1AzIxNAMyMTMDMjEyAzIxMQMyMTADMjA5AzIwOAMyMDcDMjA2AzIwNQMyMDQDMjAzAzIwMgMyMDADMTk5AzE5OAMxOTcDMTk2AzE5NQMxOTQDMTkzAzE5MgMxOTEDMTkwAzE4OQMxODgDMTg2AzE4NQMxODQDMTgyAzE4MQMxODADMTc5AzE3OAMxNzYDMTc1AzE3NBQrA0VnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIGDw8WAh4EVGV4dAUUICggUmFuZ2luZyAxIC0gMjg1IClkZAIIDxAPFgQfAAUFcXR5cGUfAWdkEBUCClNUQVJSRUQgICAKVU5TVEFSUkVEIBUCClNUQVJSRUQgICAKVU5TVEFSUkVEIBQrAwJnZ2RkAgsPDxYCHgdWaXNpYmxlaGRkAgwPPCsACwEADxYCHwNoZGRkfVROsZ5nfGl8S7f0r807YW6t0yFjYphxpv+IIAfvnfg=",
                         "__VIEWSTATEGENERATOR": "4F7831D1",
                         "__EVENTVALIDATION": "/wEdAExHJv3eUtnlTbn630FwPUHd80pEf/0+mdVHMqkT9cigOIbyrRJAvHpFy1Az4N+96MZSRQ1Yc/Y29LObIyzQnUQQE2x6ZKe/2hHX1GmqvuOqJRmsAhHGg+OigunnAjV9ttytXJsNMigPpMXLY4RRyOvlH6ciPjTCX9XCGBYfDxVdRRnqQx7BQ6tPIWFp54cifsFlJdLXn2vxeF4wQARCKP0FbXGspMymDdbcKB1+SDE8tlKvAPtOIoZop443iFX+og8GEJrvp6YHZyFvx18S/nuMgaLa1siGaAyHC8X0cXy4x8c0besgTl7cmgM/Th32iDGR5HfQkd1dWartdT9PSoArUKOdYGg/HNeuihqdRP16YOMNSs3of17X6NfGb+WJgTvn0gkivwMFJrovmlrMThEVT65+Fw86FG48dqB+cABO+eJL+DSIGGX7AuuZpRdz5CxcJ1jEbLmSZZ0TG3rHxlcVG+X6oG7t8FW955Xyu/WOyhYkociqsm+3woL7upAChYx2PmNSVjNfD91Zm97HbPF+JJauIEzluQphn3emg64It5FGPlGmg6qenBROiJyGoRe9Y9ZI9OaOzP0B2KpeMm5ELLbS4MmbgEjcJZoIVZnAvH6ksX4NQFmM8WxKJPDebKlKfrpE1Ex/adFW3S2aVvbAH2WbKQGJ6ljSznP3tN9XqH7LNQbgLw8DCPqT1cdMGXYBaxD1UH5OSG9yYe0o+IsE37U4EqD7XCU5xq3HqaiYtq4aaL2YhetTR7YHuxzvE75IVgYSv2hA4Qp8g4/ppw2zVJAt3Qhp5r5jEY0MBYikAl0QxsnG1hW1ibTAHhlF9c/6JHUxov7Kr3pbMwshhhTgU8xYm8z3BWOR30zlWzDCvYNpsDdPujrUIMNqeveTzEQZw7boXJ9MXDqKL9Gl3doPY7b38eYowA8v0wl1r/WObdaPZoV9kOYYcvd6h0eHRouqD5EiDhSSL4vcZRLd2SEPbGIhGKmeXIgtGsVSYhNUIMKrOJR6TSV8tiJujKL6AR9/94wE+nrLj3DIjSSNLsh0q3en9EcXbpH+u0ihkm93EXado3PFrBHS25ohCbvIscxLRzvCxD+5S0TD6r6hUCq4INmFVu23AEdY6pKQmaFib+AvHB53eDh/OgggGRvEkZgfvgGLVDX/OjsxJprawZbpuWlimjEgmncNVRoFrhoYErJ8Tuq3AJ+OCMLnVxp8JE/xGnrSQkS1m5sKxP9bFijaXj2fzFY0u/KyG28K+H3XEQ6rMu8BxnVdQboGt4GSrLymTEILiNYb9QNC4zykhw6+NnxVN4NvqAS7qcaB7GjuqvMmVigf0U9I8bZZmmRuEJO5Dawu0RS3S7Xj3ZbZpnkz3ZXh4YSSEAANljis3XqzENRcmy2yDiO/s5q3wWi8suG6WgKAzIe8d9vRMU9XJLsNqmM1KQxPUrYwQPegCeI9zCiY8MabRRrBsDcH48wlF/tIadIV1iFl9ZkVbSaLGWepwlAMvLjaZtdRCllKM6UGH38qAQTr8Jvbeqyed4E5edEmEPGutrje+KZsdKm0nvY0CFdiJMsyaQgT14yxPwEA8tlFImc8MKODKBr+XKEa1NQ/WMskeKo19Gyidl+m11dTkPlOC9AFGc3wIk8D/E/1mbPA7U+5Oyj5USaD/y6qkrc=",
                         "q": "",
                         "domains": "rajyasabha.nic.in",
                         "sitesearch": "rajyasabha.nic.in",
                         "DRSession": str(session),
                         "TxtQno": "",
                         "DRQtype": "STARRED   "}
            # print(form_data)
            yield scrapy.FormRequest(
                    response.request.url,
                    formdata=form_data,
                    callback=self.parse_max_question
                )
    
    def parse_max_question(self, response):
            max_questions = int(response.css("span[id=LabelRange]::text").extract()[0].split('-')[1][:-2].strip())
            for current_question in range(1,max_questions+1): #Specify the range of questions here
                query = {"question_number": response.css("select[name='DRSession'] > option[selected='selected']::text").extract_first()+"_"+str(current_question)}
                print(query)
                if self.collection.find(query).count() > 0:
                    continue
                
                form_data = {"__EVENTTARGET": "",
                             "__EVENTARGUMENT": "",
                             "__LASTFOCUS": "",
                             "__VIEWSTATE": "/wEPDwUKLTQxMjkyMjY5NQ9kFgICAQ9kFgoCAw8QDxYEHg1EYXRhVGV4dEZpZWxkBQZzZXNfbm8eC18hRGF0YUJvdW5kZ2QQFUUDMjQ4AzI0NwMyNDYDMjQ1AzI0NAMyNDMDMjQyAzI0MQMyNDADMjM5AzIzOAMyMzcDMjM2AzIzNQMyMzQDMjMzAzIzMgMyMzADMjI5AzIyOAMyMjcDMjI2AzIyNQMyMjQDMjIzAzIyMgMyMjEDMjIwAzIxOQMyMTgDMjE3AzIxNQMyMTQDMjEzAzIxMgMyMTEDMjEwAzIwOQMyMDgDMjA3AzIwNgMyMDUDMjA0AzIwMwMyMDIDMjAwAzE5OQMxOTgDMTk3AzE5NgMxOTUDMTk0AzE5MwMxOTIDMTkxAzE5MAMxODkDMTg4AzE4NgMxODUDMTg0AzE4MgMxODEDMTgwAzE3OQMxNzgDMTc2AzE3NQMxNzQVRQMyNDgDMjQ3AzI0NgMyNDUDMjQ0AzI0MwMyNDIDMjQxAzI0MAMyMzkDMjM4AzIzNwMyMzYDMjM1AzIzNAMyMzMDMjMyAzIzMAMyMjkDMjI4AzIyNwMyMjYDMjI1AzIyNAMyMjMDMjIyAzIyMQMyMjADMjE5AzIxOAMyMTcDMjE1AzIxNAMyMTMDMjEyAzIxMQMyMTADMjA5AzIwOAMyMDcDMjA2AzIwNQMyMDQDMjAzAzIwMgMyMDADMTk5AzE5OAMxOTcDMTk2AzE5NQMxOTQDMTkzAzE5MgMxOTEDMTkwAzE4OQMxODgDMTg2AzE4NQMxODQDMTgyAzE4MQMxODADMTc5AzE3OAMxNzYDMTc1AzE3NBQrA0VnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIGDw8WAh4EVGV4dAUUICggUmFuZ2luZyAxIC0gMTIwIClkZAIIDxAPFgQfAAUFcXR5cGUfAWdkEBUCClNUQVJSRUQgICAKVU5TVEFSUkVEIBUCClNUQVJSRUQgICAKVU5TVEFSUkVEIBQrAwJnZ2RkAgsPDxYCHgdWaXNpYmxlaGRkAgwPPCsACwEADxYCHwNoZGRk0c9hzgLCf6lRoafOvxEkmBTcCfMPMZtzQVdvVlmW2Tg=",
                             "__VIEWSTATEGENERATOR": "4F7831D1",
                             "__EVENTVALIDATION": "/wEdAEx+OW1T5XEyQns9EgFUvpG/80pEf/0+mdVHMqkT9cigOIbyrRJAvHpFy1Az4N+96MZSRQ1Yc/Y29LObIyzQnUQQE2x6ZKe/2hHX1GmqvuOqJRmsAhHGg+OigunnAjV9ttytXJsNMigPpMXLY4RRyOvlH6ciPjTCX9XCGBYfDxVdRRnqQx7BQ6tPIWFp54cifsFlJdLXn2vxeF4wQARCKP0FbXGspMymDdbcKB1+SDE8tlKvAPtOIoZop443iFX+og8GEJrvp6YHZyFvx18S/nuMgaLa1siGaAyHC8X0cXy4x8c0besgTl7cmgM/Th32iDGR5HfQkd1dWartdT9PSoArUKOdYGg/HNeuihqdRP16YOMNSs3of17X6NfGb+WJgTvn0gkivwMFJrovmlrMThEVT65+Fw86FG48dqB+cABO+eJL+DSIGGX7AuuZpRdz5CxcJ1jEbLmSZZ0TG3rHxlcVG+X6oG7t8FW955Xyu/WOyhYkociqsm+3woL7upAChYx2PmNSVjNfD91Zm97HbPF+JJauIEzluQphn3emg64It5FGPlGmg6qenBROiJyGoRe9Y9ZI9OaOzP0B2KpeMm5ELLbS4MmbgEjcJZoIVZnAvH6ksX4NQFmM8WxKJPDebKlKfrpE1Ex/adFW3S2aVvbAH2WbKQGJ6ljSznP3tN9XqH7LNQbgLw8DCPqT1cdMGXYBaxD1UH5OSG9yYe0o+IsE37U4EqD7XCU5xq3HqaiYtq4aaL2YhetTR7YHuxzvE75IVgYSv2hA4Qp8g4/ppw2zVJAt3Qhp5r5jEY0MBYikAl0QxsnG1hW1ibTAHhlF9c/6JHUxov7Kr3pbMwshhhTgU8xYm8z3BWOR30zlWzDCvYNpsDdPujrUIMNqeveTzEQZw7boXJ9MXDqKL9Gl3doPY7b38eYowA8v0wl1r/WObdaPZoV9kOYYcvd6h0eHRouqD5EiDhSSL4vcZRLd2SEPbGIhGKmeXIgtGsVSYhNUIMKrOJR6TSV8tiJujKL6AR9/94wE+nrLj3DIjSSNLsh0q3en9EcXbpH+u0ihkm93EXado3PFrBHS25ohCbvIscxLRzvCxD+5S0TD6r6hUCq4INmFVu23AEdY6pKQmaFib+AvHB53eDh/OgggGRvEkZgfvgGLVDX/OjsxJprawZbpuWlimjEgmncNVRoFrhoYErJ8Tuq3AJ+OCMLnVxp8JE/xGnrSQkS1m5sKxP9bFijaXj2fzFY0u/KyG28K+H3XEQ6rMu8BxnVdQboGt4GSrLymTEILiNYb9QNC4zykhw6+NnxVN4NvqAS7qcaB7GjuqvMmVigf0U9I8bZZmmRuEJO5Dawu0RS3S7Xj3ZbZpnkz3ZXh4YSSEAANljis3XqzENRcmy2yDiO/s5q3wWi8suG6WgKAzIe8d9vRMU9XJLsNqmM1KQxPUrYwQPegCeI9zCiY8MabRRrBsDcH48wlF/tIadIV1iFl9ZkVbSaLGWepwlAMvLjaZtdRCllKM6UGH38qAQTr8Jvbeqyed4E5edEmEPGutrje+KZsdKm0nvY0CFdiJMsyaQgT14yxPwEA8tlFImc8MKODKBr+XKEa1NQ/WMskeKo19Gyidl+m11dT4BvHBnAiWLsDycMIHe4s1JoZKZ5TUwhxj8de5kiD0jY=",
                             "q": "",
                             "domains": "rajyasabha.nic.in",
                             "sitesearch": "rajyasabha.nic.in",
                             "DRSession": response.css("select[name='DRSession'] > option[selected='selected']::text").extract_first(),
                             "TxtQno": str(current_question),
                             "DRQtype": "STARRED   ",
                             "Button2": "Submit"
                             }
                # print(form_data)
                yield scrapy.FormRequest(
                    response.request.url,
                    formdata=form_data,
                    callback=self.parse_question_list,
                    dont_filter = True
                )

    def parse_question_list(self, response):
        form_data = {
            "__EVENTTARGET": "DG1$_ctl3$Hyperlink1",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": response.css("input[name='__VIEWSTATE']::attr(value)").extract_first(),
            "__VIEWSTATEGENERATOR": response.css("input[name='__VIEWSTATEGENERATOR']::attr(value)").extract_first(),
            "__EVENTVALIDATION": response.css("input[name='__EVENTVALIDATION']::attr(value)").extract_first(),
            "q": "",
            "domains": "rajyasabha.nic.in",
            "sitesearch": "rajyasabha.nic.in",
            "DRSession": response.css("select[name='DRSession'] > option[selected='selected']::text").extract_first(),
            "TxtQno": response.css("a#DG1_Hyperlink1_0::text").extract_first(),
            "DRQtype": "STARRED   "
        }
        print(form_data)
        yield scrapy.FormRequest(
                response.request.url,
                formdata=form_data,
                meta = {"form_data":form_data},
                callback=self.parse_question,
                dont_filter = True
            )
    
    def parse_question(self,response):
        # open_in_browser(response)
        item = RajyaSabhaItem()
        item['session'] = response.request.meta['form_data']['DRSession']
        item['question_number'] = item['session']+"_"+str(response.request.meta['form_data']['TxtQno'])
        item['question_type'] = self.starred[self.current_star_index].rstrip()
        item['date'] = response.css("span#Label6::text").extract_first()
        item['ministry'] = response.css("span#Label1::text").extract_first()
        item['subject'] = response.css("font[color=Blue]::text").extract_first()
        item['members'] = response.css("span#LabMp::text").extract()
        item['text'] = '\n'.join([x.rstrip() for x in response.css('table#Table2 *::text').extract()])
        item['meta'] = {"fetched_on":str(datetime.datetime.now())}
        item['english_doc'] = response.css("a[href*='annex']::attr(href)").extract_first()
        item['hindi_doc'] = response.css("a[href*='qhindi']::attr(href)").extract_first()
        json.dump(dict(item),open("rj.json","w"))
        yield item
    
