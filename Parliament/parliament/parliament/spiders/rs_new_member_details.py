import scrapy
from scrapy.utils.response import open_in_browser
from parliament.items import ImageItem
import pymongo
import json

class RsOldMemberDetailsSpider(scrapy.Spider):
    name = 'rs_old_member_details'
    config_file = open("config.json")
    config = json.load(config_file)
    client = pymongo.MongoClient(config["mongo_server"])
    db = client["factly_parliament_search"]
    collection = db["rs_all_member_details"]
    custom_settings = {"ITEM_PIPELINES": {'parliament.pipelines.CustomImageNamePipeline': 1},"IMAGES_STORE":"Images"}
    url = "https://rajyasabha.nic.in/rsnew/member_site/alphabeticallist_all_terms.aspx"

    def start_requests(self):
        # url = "https://rajyasabha.nic.in/rsnew/member_site/membersearch.aspx"
        url = self.url
        yield scrapy.Request(url = url, callback=self.get_details, meta={"Current_character":"J"})

    def next_requests(self,response):
        url = self.url
        current_character = response.request.meta["Current_character"]
        form_data = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$"+response.request.meta["Current_character"],
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
            "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
            "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
            "q": "",
            "domains": "rajyasabha.nic.in",
            "sitesearch": "rajyasabha.nic.in",
            "ctl00$ContentPlaceHolder1$search_name": ""}
        
        yield scrapy.FormRequest(url = url, formdata = form_data, callback=self.get_details, meta={"Current_character":current_character})

    
    def get_details(self,response):

        current_character = response.request.meta["Current_character"]
        table = response.css("table#ctl00_ContentPlaceHolder1_GridView1")
        rows = table.css("tr")[1:]
        rs_details = []
        for row in rows:
            term_details = {}
            term_details["State"] = row.css("td")[2].css("::text").extract_first().strip()
            term_details["Party"] = row.css("td")[3].css("::text").extract_first().strip()
            term_details["From"] = row.css("td")[4].css("::text")[1].extract()
            term_details["To"] = row.css("td")[4].css("::text")[3].extract()
            term_details["Reason"] = row.css("td")[5].css("::text")[1].extract()
            if row.css("td")[0].css("::text").extract_first() == '\xa0':
                rs_details[-1]["Term_details"].append(term_details)
            else:
                member_details = {}
                member_details["ID"] = current_character+row.css("td")[0].css("::text").extract_first()
                member_details["Name"] = row.css("td")[1].css("a::text").extract_first().strip()
                member_details["Term_details"] = [term_details]
                rs_details.append(member_details)
        json.dump(rs_details,open("rs_member_details"+current_character+".json","w"))
        if current_character != "J":
            current_character = chr(ord(current_character) + 1)
            yield scrapy.Request(url = self.url, callback = self.next_requests, meta = {"Current_character":current_character})

    
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

    def refresh_page(self,response):
        meta_data = response.request.meta["Data"]
        form_data = {
                "__EVENTTARGET": meta_data["ID"],
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": response.css("input#__VIEWSTATE::attr(value)").extract_first(),
                "__VIEWSTATEGENERATOR": response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first(),
                "__EVENTVALIDATION": response.css("input#__EVENTVALIDATION::attr(value)").extract_first(),
                "q": "",
                "domains": "rajyasabha.nic.in",
                "sitesearch": "rajyasabha.nic.in",
                "ctl00$ContentPlaceHolder1$TextBox2": "",
                "ctl00$ContentPlaceHolder1$search_name": ""
            }
        yield scrapy.FormRequest(url="https://rajyasabha.nic.in/rsnew/member_site/membersearch.aspx",formdata=form_data,callback=self.parse_profile,meta={"Data":meta_data})

    def parse_profile(self,response):
        meta_data = response.request.meta["Data"]
        print(meta_data)
        id = meta_data["ID"]
        image_id = id.replace("$","_").replace("View2","View1").replace("lkb","Image1")
        image_url = "https://rajyasabha.nic.in/rsnew/member_site/"+response.css("img#"+image_id+"::attr(src)").extract_first()
        if self.collection.find({"ID":meta_data["ID"]}).count() == 0:
            self.collection.insert_one(meta_data)
            yield ImageItem(image_urls = [image_url], image_name = image_url.split("/")[-1].strip(".jpg"))

        # image_url = "https://rajyasabha.nic.in/rsnew/member_site/photos/P1929.jpg"
        # tabs = response.css("div#ctl00_ContentPlaceHolder1_TabContainer1_header").css("span.ajax__tab_outer").css("::text").extract()
        # tabs = [_.strip() for _ in tabs]