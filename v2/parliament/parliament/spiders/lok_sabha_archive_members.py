import scrapy
from scrapy.utils.response import open_in_browser
import pymongo
import json
import re

class LsArchiveMembersSpider(scrapy.Spider):
    name = 'ls_archive_members'
    start_urls = ['http://loksabhaph.nic.in/Members/lokprev.aspx']
    config_file = open("config.cfg")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongodb_uri"])
    db = client["factly_parliament_search"]
    collection = db["archive_ls_members_test"]
    reference_collection = db["archive_ls_members"]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    current_letter = 0

    def parse(self, response):
        for i in range(26):
            current_url = self.start_urls[0]+'?search='+self.letters[i]
            yield scrapy.Request(url=current_url, callback=self.full_page)

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
        # open_in_browser(response)
        list_of_members = response.css("tr.odd")
        for member in list_of_members:
            member_data = {}
            member_data["name"] = member.css("td ::text")[2].extract().strip()
            member_data["party"] = member.css("td ::text")[4].extract().strip()
            try:
                member_data["constituency"] = member.css("td ::text")[5].extract().strip().split("(")[0].strip()
            except:
                member_data["constituency"] = "Nominated"
            try:
                member_data["state"] = member.css("td ::text")[5].extract().strip().split("(")[-1].strip(")")
            except:
                member_data["state"] = "Not Available"
            sessions = member.css("td ::text")[6].extract().strip().split(',')
            member_data["terms"] = []
            for session in sessions:
                session_details = {
                    "party" : "",
                    "geography" : "",
                    "session" : str(session),
                    "house" : "1",
                    "from" : "",
                    "to" : ""
                    }
                member_data["terms"].append(session_details)
            member_data["url"] = member.css("td > a ::attr(href)").extract()[0]
            member_data["MID"] = member_data["url"].split("mpsno=")[1].split("&")[0]
            if member_data["url"].find("http") == -1:
                member_data["url"] = "http://loksabhaph.nic.in/Members/"+member_data["url"]
            check_existence = self.collection.find({"MID":member_data["MID"]})
            print(member_data)
            if check_existence.count() > 0:
                continue
            else:
                self.collection.insert_one(member_data)
                if self.reference_collection.count_documents({"_id":member_data["MID"]}) == 1:
                    reference_document = self.reference_collection.find_one({"_id":member_data["MID"]})
                    member_data["dob"] = reference_document["dob"]
                    member_data["birth_place"] = reference_document["birth_place"]
                    member_data["marital_status"] = reference_document["marital_status"]
                    member_data["sons"] = reference_document["sons"]
                    member_data["daughters"] = reference_document["daughters"]
                    member_data["education"] = reference_document["education"]
                    member_data["profession"] = reference_document["profession"]
                    self.collection.update_one({"MID":member_data["MID"]},{"$set":member_data})
                else:
                    yield scrapy.Request(url = member_data["url"], callback=self.parse_profile, meta={"MID":member_data["MID"]})

    def parse_profile(self,response):
        open_in_browser(response)
        member_id = response.request.meta["MID"]
        member_details = {}
        first_table = [_.strip() for _ in response.css("table#ContentPlaceHolder1_Datagrid1").css("td.griditem2::text").extract()]
        second_table_headings = response.css("table[cellspacing='5'] > tr > td.darkerb")
        second_table_values = response.css("table[cellspacing='5'] > tr > td.griditem2")

        for i in range(len(second_table_values)):
            heading = ' '.join([_.strip() for _ in second_table_headings[i].css('::text').extract()])
            value = ' '.join([_.strip() for _ in second_table_values[i].css('::text').extract()])
            
            if heading == 'Date of Birth':
                member_details["dob"] = value
            elif heading == 'Place of Birth':
                member_details["birth_place"] = value
            elif heading == 'Marital Status':
                member_details["marital_status"] = value
            elif heading == 'No. of Sons':
                member_details["sons"] = value
            elif heading == 'No.of Daughters':
                member_details["daughters"] = value
            elif heading == 'Educational Qualifications':
                member_details["education"] = value
            elif heading == 'Profession':
                member_details["profession"] = value
        self.collection.update_one({"ID":member_id},{"$set":member_details})
  