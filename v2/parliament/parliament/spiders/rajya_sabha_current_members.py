# -*- coding: utf-8 -*-
import scrapy
from parliament.items import ImageItem
import pymongo
import json

class RajyaSabhaCurrentMembersSpider(scrapy.Spider):
    name = 'rajya_sabha_current_members'
    # allowed_domains = ['https://rajyasabha.nic.in/rsnew/member_site/memberlist.aspx']
    start_urls = ['https://rajyasabha.nic.in/rsnew/member_site/memberlist.aspx']
    custom_settings = {"ITEM_PIPELINES": {'parliament.pipelines.CustomImageNamePipeline': 1},"IMAGES_STORE":"Images"}
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongodb_uri"])
    db = client["factly_parliament_search"]
    collection = db["rs_members_test"]

    def parse(self, response):
        pinks = response.css('tr[bgcolor="Pink"]')
        whites = response.css('tr[bgcolor="White"]')
        all_rows = pinks + whites
        list_req_params = {
            "__EVENTARGUMENT":"",
            "__EVENTTARGET":"ctl00$ContentPlaceHolder1$GridView2$ctl05$lkb",
            "__LASTFOCUS":"",
            "__VIEWSTATE":response.css("input#__VIEWSTATE::attr(value)").extract_first(),
            "__VIEWSTATEGENERATOR":"DD5CA277",
            "ctl00$ContentPlaceHolder1$TextBox2":"",
            "ctl00$ContentPlaceHolder1$search_name":"",
            "domains":"rajyasabha.nic.in",
            "q":"",
            "sitesearch":"rajyasabha.nic.in"
            }
        for row in all_rows[:5]:
            member_details = {}
            member_details["name"] = row.css("td > font")[1].css("a::text").extract_first()
            member_details["party"] = row.css("td > font")[2].css("::text").extract_first()
            member_details["state"] = row.css("td > font")[3].css("::text").extract_first()
            member_details["MID"] = row.css("td > font > a::attr(id)").extract_first().split("_")[3]
            member_link = row.css("td > font > a::attr(id)").extract_first().replace("_","$")
            list_req_params["__EVENTTARGET"] = member_link
            print(member_link)
            yield scrapy.FormRequest(url = "https://rajyasabha.nic.in/rsnew/member_site/memberlist.aspx", formdata=list_req_params, callback=self.parse_profile, meta={"member_details":member_details}, dont_filter=True, method="POST")
        # for member in pink_id_list[:2]:
        #     list_req_params["__EVENTTARGET"] = member.replace("_","$")
        #     print(list_req_params["__EVENTTARGET"])
        #     yield scrapy.FormRequest(url = "https://rajyasabha.nic.in/rsnew/member_site/memberlist.aspx", formdata=list_req_params, callback=self.parse_profile, meta={"ID":member.split("_")[3]}, dont_filter=True)
        # for member in white_id_list[:2]:
        #     list_req_params["__EVENTTARGET"] = member.replace("_","$")
        #     print(list_req_params["__EVENTTARGET"])
        #     yield scrapy.FormRequest(url = "https://rajyasabha.nic.in/rsnew/member_site/memberlist.aspx", formdata=list_req_params, callback=self.parse_profile, meta={"ID":member.split("_")[3]}, dont_filter=True)
        
    def parse_profile(self, response):
        # print(response.request.meta["member_details"])
        member_details = response.request.meta["member_details"]
        print(response.request)
        member_details["html"] = response.css("div#right_pnl").extract_first()
        member_details["image_url"] = "https://rajyasabha.nic.in/rsnew/member_site/"+response.css("img#ctl00_ContentPlaceHolder1_GridView1_ctl02_Image1::attr(src)").extract_first()
        self.collection.insert_one(member_details)
        yield ImageItem(image_urls = [member_details["image_url"]], image_name = member_details["MID"])


# req_fields = {
#     "__EVENTARGUMENT":"",
#     "__EVENTTARGET":"ctl00$ContentPlaceHolder1$GridView2$ctl05$lkb",
#     "__LASTFOCUS":"",
#     "__VIEWSTATE":response.css("input#__VIEWSTATE::attr(value)").extract_first(),
#     "__VIEWSTATEGENERATOR":"DD5CA277",
#     "ctl00$ContentPlaceHolder1$TextBox2":"",
#     "ctl00$ContentPlaceHolder1$search_name":"",
#     "domains":"rajyasabha.nic.in",
#     "q":"",
#     "sitesearch":"rajyasabha.nic.in"
#     }