# -*- coding: utf-8 -*-
import scrapy
from parlens.items import Members
import re
import datetime
import json

class LokSabhaCurrentMembers(scrapy.Spider):
    name = 'ls_current_members'
    start_urls = ['http://loksabhaph.nic.in/Members/AlphabeticalList.aspx']

    custom_settings = { 
        "ITEM_PIPELINES": {
            'parlens.pipelines.members.NameCleaner': 10,
            'parlens.pipelines.members.EducationCleaner': 20,
            'parlens.pipelines.members.MaritalCleaner': 30,
            'parlens.pipelines.members.ProfessionCleaner': 40,
            'parlens.pipelines.lsmembers.DOBCleaner': 50,
            'parlens.pipelines.lsmembers.EmailCleaner': 60,
            'parlens.pipelines.lsmembers.ChildrenCleaner': 70
        }
    }
    
    def parse(self,response):
        mp_url_list = response.css("tr.odd > td > a ::attr(href)").extract()[1::2]
        
        for mp_url in mp_url_list:
            url = "http://loksabhaph.nic.in/Members/"+mp_url
            yield scrapy.Request(url=url, callback=self.parse_profile)

    def parse_profile(self,response):
        item = {}
        url = response.url
        item['LSID'] = int(url.split('=')[1])

        item['name'] = response.css("td.gridheader1::text").extract()[0].strip()
        first_table = [_.strip() for _ in response.css("table#ContentPlaceHolder1_Datagrid1").css("td.griditem2::text").extract()]

        constituency = first_table[0]
        state = re.findall("\(.*\)",constituency)[0].strip('()')
        item['geography'] = constituency.replace(re.findall("\(.*\)",constituency)[0],"").strip()

        item['state'] = state.split('(')[-1]
        item['party'] = first_table[1]
        
        
        item['email'] = list()
        for _ in first_table[2:]:
            if _ != "":
                item['email'].append(_)

        second_table_headings = response.css("table[cellspacing='5'] > tr > td.darkerb")
        second_table_values = response.css("table[cellspacing='5'] > tr > td.griditem2")

        for i in range(len(second_table_values)):
            heading = ' '.join([_.strip() for _ in second_table_headings[i].css('::text').extract()])
            value = ' '.join([_.strip() for _ in second_table_values[i].css('::text').extract()])
            
            if heading == 'Date of Birth':
                item['dob'] = value
            elif heading == 'Place of Birth':
                item['birth_place'] = value
            elif heading == 'Marital Status':
                item['marital_status'] = value
            elif heading == 'No. of Sons':
                item['sons'] = value
            elif heading == 'No.of Daughters':
                item['daughters'] = value
            elif heading == 'Educational Qualifications':
                item['education'] = value
            elif heading == 'Profession':
                item['profession'] = value
            elif heading == 'Permanent Address':
                item['phone'] = re.findall("[0-9]{11}|[0-9]{10}", value)

        yield Members(
            LSID = item['LSID'],
            name = item['name'],
            geography = item['geography'],
            state = item['state'],
            party = item['party'],
            dob = item['dob'] if 'dob' in item else None,
            birth_place = item['birth_place'] if 'birth_place' in item else None,
            marital_status = item['marital_status'] if 'marital_status' in item else None,
            sons = item['sons'] if 'sons' in item else None,
            daughters = item['daughters'] if 'daughters' in item else None,
            education = item['education'] if 'education' in item else None,
            profession = item['profession'] if 'profession' in item else None,
            phone = item['phone'] if 'phone' in item else None,
            email = item['email']
        )