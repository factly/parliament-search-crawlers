import scrapy
from scrapy.utils.response import open_in_browser
from parliament.items import ImageItem
import pymongo
import json
import os


class RsOldMemberDetailsSpider(scrapy.Spider):
    name = 'rs_old_member_details'
    config_file = open("config.json")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["rs_all_member_details"]
    custom_settings = {"ITEM_PIPELINES": {
        'parliament.pipelines.CustomImageNamePipeline': 1}, "IMAGES_STORE": "Images"}
    url = "https://rajyasabha.nic.in/rsnew/member_site/alphabeticallist_all_terms.aspx"
    data_folder = "RS_Data_2"
    def start_requests(self):
        # url = "https://rajyasabha.nic.in/rsnew/member_site/membersearch.aspx"
        url = self.url
        yield scrapy.Request(url=url, callback=self.next_requests, meta={"Current_character": "X"})

    def next_requests(self, response):
        url = self.url
        current_character = response.request.meta["Current_character"]
        form_data = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$"+current_character,
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
            "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
            "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
            "q": "",
            "domains": "rajyasabha.nic.in",
            "sitesearch": "rajyasabha.nic.in",
            "ctl00$ContentPlaceHolder1$search_name": ""}

        yield scrapy.FormRequest(url=url, formdata=form_data, callback=self.get_details, meta={"Current_character": current_character})

    def get_details(self, response):
        current_character = response.request.meta["Current_character"]
        table = response.css("table#ctl00_ContentPlaceHolder1_GridView1")
        rows = table.css("tr")[1:]
        rs_details = []
        for row in rows:
            try:
                term_details = {}
                term_details["State"] = row.css("td")[2].css(
                    "::text").extract_first().strip()
                term_details["Party"] = row.css("td")[3].css(
                    "::text").extract_first().strip()
                term_details["From"] = row.css("td")[4].css("::text")[1].extract()
                term_details["To"] = row.css("td")[4].css("::text")[3].extract()
                term_details["Reason"] = row.css(
                    "td")[5].css("::text")[1].extract()
                if row.css("td")[0].css("::text").extract_first() == '\xa0':
                    # print(term_details)
                    rs_details[-1]["Term_details"].append(term_details)
                else:
                    member_details = {}
                    member_details["ID"] = current_character + \
                        row.css("td")[0].css("::text").extract_first()
                    member_details["Name"] = row.css("td")[1].css(
                        "a::text").extract_first().strip()
                    member_details["Term_details"] = [term_details]
                    print(member_details["Name"])
                    rs_details.append(member_details)
            except:
                term_details = {}
                term_details["State"] = "Not Available"
                term_details["Party"] = "Not Available"
                term_details["From"] = "Not Available"
                term_details["To"] = "Not Available"
                term_details["Reason"] = "Not Available"
                member_details["ID"] = current_character + row.css("td")[0].css("::text").extract_first()
                member_details["Name"] = row.css("td")[1].css("a::text").extract_first().strip()
                member_details["Term_details"] = [term_details]
                print(member_details["Name"])
                rs_details.append(member_details)
                
        json.dump(rs_details, open(self.data_folder+"/rs_member_details" + current_character+".json", "w"))
        print(rs_details)
        if current_character != "Z":
            current_character = chr(ord(current_character) + 1)
            yield scrapy.Request(url=self.url, callback=self.next_requests, meta={"Current_character": current_character,"Last_done":"False"})
        else:
            self.write_to_db()
            yield scrapy.Request(url=self.url, callback=self.next_requests, meta={"Current_character": "A","Last_done":"True"})

    def write_to_db(self):
        files = os.listdir(self.data_folder)
        for file in files:
            file_name = self.data_folder+"/"+file
            file_data = json.load(open(file_name))
            if file_data!= []:
                self.collection.insert_many(file_data)

    def traverse_profiles(self,response):
        current_character = response.request.meta["Current_character"]
        table = response.css("table#ctl00_ContentPlaceHolder1_GridView1")
        rows = table.css("tr")[1:]
        for row in rows:
            if row.css("td")[0].css("::text").extract_first() != '\xa0':
                id = current_character + row.css("td")[0].css("::text").extract_first()
                anchor_id = row.css("a::attr(id)").extract_first().replace("_","$")
                form_data = {
                    "__EVENTTARGET": anchor_id,
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS": "",
                    "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
                    "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
                    "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
                    "q": "",
                    "domains": "rajyasabha.nic.in",
                    "sitesearch": "rajyasabha.nic.in",
                    "ctl00$ContentPlaceHolder1$search_name": ""
                }
                yield scrapy.FormRequest(url="https://rajyasabha.nic.in/rsnew/member_site/alphabeticallist_all_terms.aspx", 
                formdata=form_data, callback = self.goto_profile, meta = {"ID":id})

    def goto_profile(self,response):
        for tab_id in range(1,8):
            form_data = {
                    "ctl00$toolkitscriptmanager1": "ctl00$ContentPlaceHolder1$UpdatePanel1|ctl00$ContentPlaceHolder1$TabContainer1",
                    "ctl00_ContentPlaceHolder1_TabContainer1_ClientState": {"ActiveTabIndex":0,"TabEnabledState":["true","true","true"],"TabWasLoadedOnceState":["false","false","false"]},
                    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$TabContainer1",
                    "__EVENTARGUMENT": {"activeTabChanged":tab_id},
                    "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
                    "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
                    "__VIEWSTATEENCRYPTED": "",
                    "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
                    "q": "",
                    "domains": "rajyasabha.nic.in",
                    "sitesearch": "rajyasabha.nic.in",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$eduext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$proext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$peraext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$presaext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$posiext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$bookext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$sociext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$sprtext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$ctryext_ClientState": "true",
                    "ctl00$ContentPlaceHolder1$TabContainer1$TabPanel2$DetailsView2$othiext_ClientState": "true",
                    "__ASYNCPOST": "true"
                }
            yield scrapy.FormRequest(url="https://rajyasabha.nic.in/rsnew/member_site/alphabeticallist_all_terms.aspx", formdata=form_data, 
            callback = self.goto_tab, meta = {"ID":response.request.meta["ID"], "Tab":tab_id})
    
    def goto_tab(self,response):
        tab_id = response.request.meta["Tab"]
        id = response.request.meta["ID"]
        if tab_id == 1:
            print("Meow")

    # def get_ids(self,response):
    #     rows_pink = response.css("tr[bgcolor*='Pink']")
    #     rows_white = response.css("tr[bgcolor*='White']")
    #     rows = rows_pink + rows_white
        # ids = response.css("table#ctl00_ContentPlaceHolder1_GridView2").css("a::attr(id)").extract()
        # ids = [_.replace("_","$") for _ in ids]
        # for i,row in enumerate(rows[:5]):
            # id = row.css("a::attr(id)").extract_first()
            # id = id.replace("_","$")
            # meta_data = {}
            # meta_data["ID"] = row.css("a::attr(id)").extract_first()
            # meta_data["ID"] = meta_data["ID"].replace("_","$")
            # meta_data["Name"] = row.css("td")[2].css("a::text").extract_first()
            # meta_data["Party"] = row.css("td")[3].css("font::text").extract_first().strip()
            # meta_data["State"] = row.css("td")[4].css("font::text").extract_first().strip()
            # yield scrapy.Request(url="https://rajyasabha.nic.in/rsnew/member_site/membersearch.aspx",callback=self.refresh_page,meta={"Data":meta_data})
            # form_data = {
            #     "__EVENTTARGET": meta_data["ID"],
            #     "__EVENTARGUMENT": "",
            #     "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
            #     "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
            #     "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
            #     "q": "",
            #     "domains": "rajyasabha.nic.in",
            #     "sitesearch": "rajyasabha.nic.in",
            #     "ctl00$ContentPlaceHolder1$TextBox2": "",
            #     "ctl00$ContentPlaceHolder1$search_name": ""
            # }

    # def refresh_page(self, response):
    #     meta_data = response.request.meta["Data"]
    #     form_data = {
    #         "__EVENTTARGET": meta_data["ID"],
    #         "__EVENTARGUMENT": "",
    #         "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
    #         "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
    #         "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
    #         "q": "",
    #         "domains": "rajyasabha.nic.in",
    #         "sitesearch": "rajyasabha.nic.in",
    #         "ctl00$ContentPlaceHolder1$TextBox2": "",
    #         "ctl00$ContentPlaceHolder1$search_name": ""
    #     }
    #     yield scrapy.FormRequest(url="https://rajyasabha.nic.in/rsnew/member_site/membersearch.aspx", formdata=form_data, callback=self.parse_profile, meta={"Data": meta_data})

    # def parse_profile(self, response):
    #     meta_data = response.request.meta["Data"]
    #     print(meta_data)
    #     id = meta_data["ID"]
    #     image_id = id.replace("$", "_").replace(
    #         "View2", "View1").replace("lkb", "Image1")
    #     image_url = "https://rajyasabha.nic.in/rsnew/member_site/" + \
    #         response.css("img#"+image_id+"::attr(src)").extract_first()
    #     if self.collection.find({"ID": meta_data["ID"]}).count() == 0:
    #         self.collection.insert_one(meta_data)
    #         yield ImageItem(image_urls=[image_url], image_name=image_url.split("/")[-1].strip(".jpg"))

        # image_url = "https://rajyasabha.nic.in/rsnew/member_site/photos/P1929.jpg"
        # tabs = response.css("div#ctl00_ContentPlaceHolder1_TabContainer1_header").css("span.ajax__tab_outer").css("::text").extract()
        # tabs = [_.strip() for _ in tabs]
