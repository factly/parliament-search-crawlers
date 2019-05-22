# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from parliament.items import ImageItem
import pymongo
import json
import re
from word2number import w2n



class LsNewMemberMoreDetailsSpider(scrapy.Spider):
    name = 'ls_new_member_details'
    config_file = open("config.json")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["ls_all_member_urls"]
    custom_settings = {"ITEM_PIPELINES": {'parliament.pipelines.CustomImageNamePipeline': 1},"IMAGES_STORE":"Images"}
    def start_requests(self):
        print("Starting")
        compatible_members = self.collection.find({
            '$or': [
                {'Sessions': '13'}, 
                {'Sessions': '14'}, 
                {'Sessions': '15'}, 
                {'Sessions': '16'}
                ]
                })
        print("Results:",compatible_members.count())
        for member in compatible_members:
            url = member["URL"]
            print(url)
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
        image_url = response.css("img#ContentPlaceHolder1_Image1 ::attr( src)").extract_first()
        yield ImageItem(image_urls = [image_url], image_name = response.request.meta["ID"])


class Ls12MemberMoreDetailsSpider(scrapy.Spider):
    name = 'ls_12_member_details'
    config_file = open("config.json")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["ls_all_member_urls"]
    custom_settings = {"ITEM_PIPELINES": {'parliament.pipelines.CustomImageNamePipeline': 1},"IMAGES_STORE":"Images"}
    def start_requests(self):
        print("Starting")
        compatible_members = self.collection.find(
            {"$and": [
                {"Sessions": {"$nin": ["13", "14", "15", "16"]}}, 
                {"Sessions": "12"}]})
        print("Results:",compatible_members.count())
        for member in compatible_members:
            url = member["URL"]
            print(url)
            yield scrapy.Request(url = url, callback=self.parse_profile, meta={"ID":member["ID"]})

    def parse_profile(self,response):

        member_id = response.request.meta["ID"]
        member_details = {}
        member_details["Name"] = response.css("font[size='4']::text").extract_first().title()
        
        details = list(response.css("font")[3].css("::text").extract())
        details = [_.strip() for _ in details]

        if "Date of Birth" in details:
            member_details["DOB"] = details[details.index("Date of Birth")+2]
        if "Place of Birth" in details:
            member_details["Birth_place"] = details[details.index("Place of Birth")+2]
        if "Marital Status" in details:
            member_details["Marital_Status"] = details[details.index("Marital Status")+2].split()[0]
        if "Children" in details:
            children_details = details[details.index("Children")+2].split()
            children_details = [_.rstrip("s") for _ in children_details]
            if "son" in children_details:
                sons = children_details[children_details.index("son") - 1]
                member_details["Sons"] = w2n.word_to_num(sons)
            if "daughter" in children_details:
                daughters = children_details[children_details.index("daughter") - 1]
                member_details["Daughters"] = w2n.word_to_num(daughters)
        if "Educational Qualifications" in details:
            education = details[details.index("Educational Qualifications")+2]
            education = education.replace("\r","").replace("\n","")
            member_details["Education"] = education
        if "Profession" in details:
            member_details["Profession"] = details[details.index("Profession")+2]            

            print(member_details)
            
        self.collection.update_one({"ID":member_id},{"$set":member_details})
        image_url = response.url.replace("htm","jpg")
        yield ImageItem(image_urls = [image_url], image_name = response.request.meta["ID"])


class Ls11MemberMoreDetailsSpider(scrapy.Spider):
    name = 'ls_11_member_details'
    config_file = open("config.json")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["ls_all_member_urls"]
    custom_settings = {"ITEM_PIPELINES": {'parliament.pipelines.CustomImageNamePipeline': 1},"IMAGES_STORE":"Images"}
    def start_requests(self):
        print("Starting")
        compatible_members = self.collection.find(
            {"$and": [
                {"Sessions": {"$nin": ["12","13", "14", "15", "16"]}}, 
                {"Sessions": "11"}]})
        print("Results:",compatible_members.count())
        for member in compatible_members:
            url = member["URL"]
            print(url)
            yield scrapy.Request(url = url, callback=self.parse_profile, meta={"ID":member["ID"]})

    def parse_profile(self,response):

        member_id = response.request.meta["ID"]
        member_details = {}
        member_details["Name"] = response.css("font[size='5']::text").extract_first().title().strip()
        
        if len(response.css("font")) > 0:
            details = list(response.css("font[size='4']")[1].css("::text").extract())
            details = [_.strip() for _ in details]

            if "Date of Birth" in details:
                member_details["DOB"] = details[details.index("Date of Birth")+2]
            if "Place of Birth" in details:
                member_details["Birth_place"] = details[details.index("Place of Birth")+2]
            if "Marital Status" in details:
                member_details["Marital_Status"] = details[details.index("Marital Status")+2].split()[0]
            if "Children" in details:
                children_details = details[details.index("Children")+2].split()
                children_details = [_.rstrip("s") for _ in children_details]
                if "son" in children_details:
                    sons = children_details[children_details.index("son") - 1]
                    member_details["Sons"] = w2n.word_to_num(sons)
                if "daughter" in children_details:
                    daughters = children_details[children_details.index("daughter") - 1]
                    member_details["Daughters"] = w2n.word_to_num(daughters)
            if "Educational Qualifications" in details:
                education = details[details.index("Educational Qualifications")+2]
                education = education.replace("\r","").replace("\n","")
                member_details["Education"] = education
            if "Profession" in details:
                member_details["Profession"] = details[details.index("Profession")+2]            

                print(member_details)
                
            self.collection.update_one({"ID":member_id},{"$set":member_details})
            image_url = response.url.replace("htm","gif")
            yield ImageItem(image_urls = [image_url], image_name = response.request.meta["ID"])