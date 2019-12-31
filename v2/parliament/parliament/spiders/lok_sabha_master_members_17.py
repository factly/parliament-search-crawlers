# -*- coding: utf-8 -*-
import scrapy
from parliament.items import ImageItem
import pymongo
import re
import datetime

class LokSabhaMaster17Spider(scrapy.Spider):
    name = 'lok_sabha_members_master'
    start_urls = ['http://164.100.47.194/Loksabha/Members/AlphabeticalList.aspx']
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["current_ls_members"]
    custom_settings = {"ITEM_PIPELINES": {'parliament.pipelines.CustomImageNamePipeline': 1},"IMAGES_STORE":"Images/17"}
    
    def parse(self,response):
        mp_url_list = response.css("tr.odd > td > a ::attr(href)").extract()[1::2]
        
        for mp_url in mp_url_list:
            url = "http://164.100.47.194/Loksabha/Members/"+mp_url
            yield scrapy.Request(url=url, callback=self.parse_profile)

    def parse_profile(self,response):
        item = {}
        url = response.url
        item["_id"] = url.split('=')[1]
        print("ID: ",item["_id"])

        item["name"] = response.css("td.gridheader1::text").extract()[0].strip()
        first_table = [_.strip() for _ in response.css("table#ContentPlaceHolder1_Datagrid1").css("td.griditem2::text").extract()]

        constituency = first_table[0]
        state = re.findall("\(.*\)",constituency)[0].strip('()')
        constituency = constituency.replace(re.findall("\(.*\)",constituency)[0],"").strip()
        item["geography"] = constituency
        item["state"] = state.split('(')[-1]
        party = first_table[1]
        item["party"] = party
        item["terms"] = [{
            "party" : party,
            "geography" : constituency,
            "session" : "17",
            "house" : "1",
            "from" : "2019",
            "to" : "2024"
        }]
        item["email"] = []
        for _ in first_table[2:]:
            if _ != "":
                item["email"].append(_)

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
            elif heading == 'Permanent Address':
                item["phone"] = re.findall("[0-9]{11}|[0-9]{10}", value)
        previous_record = self.collection.find_one({"_id" : item['_id']})
        item["meta"] = {}
        item["meta"]["fetched_on"] = datetime.datetime.now()
        
        if previous_record == None:
            self.collection.insert_one(dict(item))
        else:
            item["meta"]["old_record"] = previous_record
            item["meta"]["old_record"]["meta"]["old_record"] = ""
            self.collection.update_one({"_id" : item["_id"]},{"$set":item})
        image_url = response.css("#ContentPlaceHolder1_Image1::attr(src)").extract_first()
        yield ImageItem(image_urls=[image_url], image_name=image_url.split("/")[-1].strip(".jpg"))