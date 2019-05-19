# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
import pymongo
import json
import re



class LsAllMemberMoreDetailsSpider(scrapy.Spider):
    name = 'ls_all_member_more_details'
    config_file = open("config.json")
    config = json.load(config_file)
    print(config["mongo_server"])
    client = pymongo.MongoClient(config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["ls_all_member_urls"]
    compatible_members = collection.find({"Session":"13"})

    def start_requests(self):
        print("Results:",self.compatible_members.count())
        for member in self.compatible_members:
            url = member["URL"]
            yield scrapy.Request(url = url, callback=self.parse_profile, meta={"ID":member["ID"]})


    # def parse(self,response):
    #     print("Results:",len(self.compatibele_members))
    #     for member in self.compatible_members:
    #         url = member["URL"]
    # #         # yield scrapy.Request(url = url, callback=self.parse_profile, meta={"ID":member["ID"]})

    def parse_profile(self,response):
        member_id = response.request.meta["ID"]
        member_details = {}
        member_details["Name"] = response.css("td.gridheader1::text").extract()[0].strip()
        first_table = [_.strip() for _ in response.css("table#ContentPlaceHolder1_Datagrid1").css("td.griditem2::text").extract()]

        constituency = first_table[0]
        state = re.findall("\(.*\)",constituency)[0].strip('()')
        constituency = constituency.replace(re.findall("\(.*\)",constituency)[0],"").strip()
        member_details["Constituency"] = constituency
        member_details["State"] = state.split('(')[-1]

        party = first_table[1]
        member_details["Party"] = party

        second_table_headings = response.css("table[cellspacing='5'] > tr > td.darkerb")
        second_table_values = response.css("table[cellspacing='5'] > tr > td.griditem2")

        for i in range(len(second_table_values)):
            heading = ' '.join([_.strip() for _ in second_table_headings[i].css('::text').extract()])
            value = ' '.join([_.strip() for _ in second_table_values[i].css('::text').extract()])
            
            if heading == 'Date of Birth':
                member_details["DOB"] = value
            elif heading == 'Place of Birth':
                member_details["Birth_place"] = value
            elif heading == 'Marital Status':
                member_details["Marital_status"] = value
            elif heading == 'No. of Sons':
                member_details["Sons"] = value
            elif heading == 'No.of Daughters':
                member_details["Daughters"] = value
            elif heading == 'Educational Qualifications':
                member_details["Education"] = value
            elif heading == 'Profession':
                member_details["Profession"] = value
            print(member_details)
        self.collection.update_one({"ID":member_id},{"$set":member_details})