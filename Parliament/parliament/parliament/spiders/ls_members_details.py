# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import re
import time
from parliament.items import MemberofParliament
import json
import pymongo

class LsMembersDetailsSpider(scrapy.Spider):
    name = 'ls_members_details'
    # allowed_domains = ['http://164.100.47.194/Loksabha/Members/AlphabeticalList.aspx']
    start_urls = ['http://164.100.47.194/Loksabha/Members/AlphabeticalList.aspx']
    config_file = open("config.json")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["members_ls_site"]
    custom_settings = {"ITEM_PIPELINES": 
    { 'parliament.pipelines.MembersPipeline': 500}
    }
    def __init__(self):
        self.members = []
        # self.data = pd.DataFrame(columns=["ID",
        #               "Name",
        #               "Constituency",
        #               "State",
        #               "Party",
        #               "DOB",
        #               "Birth_Place",
        #               "Marital_Status",
        #               "Education",
        #               "Profession",
        #               "Sons",
        #               "Daughters",
        #               "URL"])
        # self.data = self.data.fillna("Not Available")
    def parse(self, response):

        """Extract List Of All URLs"""
        # mp_id_list = [20, 4903, 4422, 4850, 4773, 4436, 4462, 4442, 4687, 4566, 3394, 4640, 4890, 4805, 4475, 4816, 4800, 4559, 4893, 4688, 4614, 4698, 4814, 4910, 4089, 4938, 4111, 4943, 4936, 4460, 394, 4707, 4851, 4907, 4930, 4738, 4904, 4920]
        mp_id_list = [4821, 4762, 4895, 7, 519, 4483, 4497, 291, 4593, 4599, 4594, 2692, 4631, 10, 4501, 4897, 4819, 2660, 3439, 4811, 4801, 4163, 197]
        # mp_url_list = response.css("tr.odd > td > a ::attr(href)").extract()
        for i in range(len(mp_id_list)):
            # url = "http://164.100.47.194/Loksabha/Members/"+mp_url_list[i]
            url = "http://164.100.47.194/Loksabha/Members/MemberBioprofile.aspx?mpsno="+str(mp_id_list[i])
            yield scrapy.Request(url=url, callback=self.parse_profile)
            # self.member_urls.append("http://164.100.47.194/Loksabha/Members/"+mp_url_list[i])
        # self.data["ID"] = mp_ids
        # self.data["URL"] = mp_urls_list
        # self.fetch_details_page()
        # self.list_length = len(self.data)
        # self.change_list = [0]*self.list_length
        # print("Yeah")
        # print(self.data.loc[0,"URL"])
        # self.data.to_excel("raw.xlsx")
        # self.fetch_details_page(0)
        
    def parse_profile(self,response):

        item = MemberofParliament()
        url = response.url
        item["id"] = url.split('=')[1]
        print("ID: ",item["id"])

        item["name"] = response.css("td.gridheader1::text").extract()[0].strip()
        first_table = [_.strip() for _ in response.css("table#ContentPlaceHolder1_Datagrid1").css("td.griditem2::text").extract()]

        constituency = first_table[0]
        state = re.findall("\(.*\)",constituency)[0].strip('()')
        constituency = constituency.replace(re.findall("\(.*\)",constituency)[0],"").strip()
        item["constituency"] = constituency
        item["state"] = state.split('(')[-1]

        party = first_table[1]
        item["party"] = party

        second_table_headings = response.css("table[cellspacing='5'] > tr > td.darkerb")
        second_table_values = response.css("table[cellspacing='5'] > tr > td.griditem2")

        for i in range(len(second_table_values)):
            heading = ' '.join([_.strip() for _ in second_table_headings[i].css('::text').extract()])
            value = ' '.join([_.strip() for _ in second_table_values[i].css('::text').extract()])
            
            if heading == 'Date of Birth':
                item["dob"] = value
            elif heading == 'Place of Birth':
                item["birth_place"] = value
            elif heading == 'Marital Status':
                item["marital_status"] = value
            elif heading == 'No. of Sons':
                item["sons"] = value
            elif heading == 'No.of Daughters':
                item["daughters"] = value
            elif heading == 'Educational Qualifications':
                item["education"] = value
            elif heading == 'Profession':
                item["profession"] = value
        yield item
        # self.members.append(dict(item))
        
    # def fetch_details_page(self,index=0):
        
    #     # print(self.data.loc[index,"URL"])
    #     yield scrapy.Request(url=self.data.loc[index,"URL"], callback=self.extract_details, meta={"index":index})
    
    # def parse(self,response):
    #     item = MemberofParliament()
    #     item["id"] = id
    #     index = response.meta["index"]
    #     print("Index: ",index)
    #     item["name"] = response.css("td.gridheader1::text").extract()[0].strip()
    #     first_table = [_.strip() for _ in response.css("table#ContentPlaceHolder1_Datagrid1").css("td.griditem2::text").extract()]

    #     constituency = first_table[0]
    #     state = re.findall("\(.*\)",constituency)[0].strip('()')
    #     constituency = constituency.replace(re.findall("\(.*\)",constituency)[0],"").strip()
    #     item["constituency"] = constituency
    #     item["state"] = state

    #     party = first_table[1]
    #     item["party"] = party

    #     second_table_headings = response.css("table[cellspacing='5'] > tr > td.darkerb")
    #     second_table_values = response.css("table[cellspacing='5'] > tr > td.griditem2")

    #     for i,heading_element in enumerate(second_table_headings):
    #         heading = ' '.join([_.strip() for _ in heading_element.css('::text').extract()])
    #         value = ' '.join([_.strip() for _ in second_table_values[i].css('::text').extract()])
            
    #         if heading == 'Date of Birth':
    #             item["dob"] = value
    #         elif heading == 'Place of Birth':
    #             item["birth_place"] = value
    #         elif heading == 'Marital Status':
    #             item["marital_status"] = value
    #         elif heading == 'No. of Sons':
    #             item["sons"] = value
    #         elif heading == 'No.of Daughters':
    #             item["daughters"] = value
    #         elif heading == 'Educational Qualifications':
    #             item["education"] = value
    #         elif heading == 'Profession':
    #             item["profession"] = value
        
    #     self.change_list[index] = 1

    #     if index < self.list_length - 1:
    #         self.fetch_details_page(index+1)
    #         return
    #     elif index == self.list_length - 1:
    #         while True:
    #             if sum(self.change_list) == self.list_length:
    #                 self.data.to_excel("Member_Details.xlsx")
    #                 yield
    #             else:
    #                 time.sleep(0.1)

        
    # def start_requests(self):


    # def parse(self, response):
        
