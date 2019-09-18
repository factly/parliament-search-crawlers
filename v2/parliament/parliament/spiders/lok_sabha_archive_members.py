# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
import pymongo
import json
import re
# from parliament.items import ParliamentItem

class LsAllMembersSpider(scrapy.Spider):
    name = 'ls_all_members'
    # allowed_domains = ['loksabhaph.nic.in/Members/lokprev.aspx']
    start_urls = ['http://loksabhaph.nic.in/Members/lokprev.aspx']
    # start_urls = ["file:///C:/Users/ishsx/Documents/GitHub/parliament-search-crawlers/Resources/Members%20_%20Lok%20Sabha.html"]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    current_letter = 0
    # start_urls[0] = start_urls[0]+"?search="+letters[current_letter]
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongodb_uri"])
    db = client["factly_parliament_search"]
    collection = db["ls_all_member_urls"]

    def parse(self, response):
        open_in_browser(response)
        for i in range(3):
            current_url = self.start_urls[0]+'?search='+self.letters[i]
            yield scrapy.Request(url=current_url, callback=self.full_page)
    # def parse(self, response):

    def full_page(self,response):
        form_data = {
            "__EVENTARGUMENT" : "",
            "__EVENTTARGET" : "ctl00$ContentPlaceHolder1$drdpages",
            "__EVENTVALIDATION" : response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
            "__LASTFOCUS" : "",
            "__VIEWSTATE" : response.css('input#__VIEWSTATE::attr(value)').extract_first(),
            "__VIEWSTATEENCRYPTED" : "",
            "__VIEWSTATEGENERATOR" : "489EEF68",
            "ctl00$ContentPlaceHolder1$ddlfile" : ".pdf",
            "ctl00$ContentPlaceHolder1$drdpages" : "5000",
            "ctl00$ContentPlaceHolder1$hidTableCount" : "",
            "ctl00$ContentPlaceHolder1$member" : "rdbtnName",
            "ctl00$ContentPlaceHolder1$txtPageNo" : "",
            "ctl00$ContentPlaceHolder1$txtSearch" : "",
            "ctl00$txtSearchGlobal" : ""
        }
        yield scrapy.FormRequest(url = response.url, formdata=form_data, callback=self.parse_member_list)

    def parse_member_list(self, response):
        open_in_browser(response)
        return
        list_of_members = response.css("tr.odd")
        for member in list_of_members:
            member_data = {}
            member_data["Name"] = member.css("td ::text")[2].extract().strip()
            member_data["Party"] = member.css("td ::text")[4].extract().strip()
            try:
                member_data["Constituency"] = member.css("td ::text")[5].extract().strip().split("(")[0].strip()
            except:
                member_data["Constituency"] = "Nominated"
            try:
                member_data["State"] = member.css("td ::text")[5].extract().strip().split("(")[-1].strip(")")
            except:
                member_data["State"] = "Not Available"
            member_data["Sessions"] = member.css("td ::text")[6].extract().strip().split(',')
            member_data["URL"] = member.css("td > a ::attr(href)").extract()[0]
            member_data["ID"] = member_data["URL"].split("mpsno=")[1].split("&")[0]
            if member_data["URL"].find("http") == -1:
                member_data["URL"] = "http://loksabhaph.nic.in/Members/"+member_data["URL"]
            check_existence = self.collection.find({"ID":member_data["ID"]})
            print(member_data)
            if check_existence.count() > 0:
                continue
            else:
                self.collection.insert_one(member_data)

class LsAllMembersDetailsSpider(scrapy.Spider):
    name = "ls_all_member_details"
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongodb_uri"])
    db = client["factly_parliament_search"]
    collection = db["ls_all_member_urls"]
    compatible_members = collection.find({"Session":"13"})
    start_urls = ["http://loksabhaph.nic.in/Members/lokprev.aspx"]

def parse(self,reaponse):
    print("Results:",len(self.compatibele_members))
    for member in self.compatible_members:
        url = member["URL"]
        yield scrapy.Request(url = url, callback=self.parse_profile, meta={"ID":member["ID"]})

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

# -*- coding: utf-8 -*-
import scrapy
from parliament.items import ImageItem
import pymongo
import re

class LokSabhaMaster17Spider(scrapy.Spider):
    name = 'lok_sabha_master_17'
    # allowed_domains = ['164.100.47.194/Loksabha/Members/AlphabeticalList.aspx']
    start_urls = ['http://164.100.47.194/Loksabha/Members/AlphabeticalList.aspx']
    client = pymongo.MongoClient("mongodb://root:ZJMNF5I4YMKO@35.200.213.251:27017/admin")#config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["lok_sabha_master_17"]
    
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
        item["constituency"] = constituency
        item["session"] = [17]
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
        self.collection.insert_one(dict(item))
        image_url = response.css("#ContentPlaceHolder1_Image1::attr(src)").extract_first()
        yield ImageItem(image_urls=[image_url], image_name=image_url.split("/")[-1].strip(".jpg"))