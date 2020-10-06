# -*- coding: utf-8 -*-
import scrapy
from parlens.items import RSMembers
import datetime
import re

class RSCurrentMembersSpider(scrapy.Spider):
    name = 'rs_current_members'
    
    start_urls = ['https://rajyasabha.nic.in/rsnew/member_site/MemlistElDate.aspx']
    
    error = open("errors.log","a+")
    error.write("\n\n\n######## Rajya Sabha Current Members Crawler "+str(datetime.datetime.now())+" ###########\n" )
    
    custom_settings = {
        "ITEM_PIPELINES": {
            'parlens.pipelines.rsmembers.DuplicateCleaner': 5, # remove already existing member based on RSID
            'parlens.pipelines.members.NameCleaner': 10, # seprate name and prefix 
            'parlens.pipelines.members.EducationCleaner': 20, # clean education field and assign value
            'parlens.pipelines.members.MaritalCleaner': 30, # clean marital field and assign appropriate value
            'parlens.pipelines.members.ProfessionCleaner': 50, # clean profession 
            'parlens.pipelines.rsmembers.DOBCleaner': 60, # convert dob into timestamp
            'parlens.pipelines.rsmembers.ChildrenCleaner': 70, # clean sons and daughters field
            'parlens.pipelines.rsmembers.GeoTermCleaner': 80, # convert geography field into GID  
            'parlens.pipelines.rsmembers.PartyTermCleaner': 90, # convert party field into PID
            'parlens.pipelines.rsmembers.TermConstructor': 100, # Construct term object and remove party and geography field
        }
    }

    def parse(self, response):
        all_rows = response.css("#ctl00_ContentPlaceHolder1_GridView2").css("tr")
        
        list_req_params = {
            "__EVENTARGUMENT":"",
            "__EVENTTARGET":"ctl00$ContentPlaceHolder1$GridView2$ctl05$lkb",
            "__LASTFOCUS":"",
            "__VIEWSTATE":response.css("input#__VIEWSTATE::attr(value)").extract_first(),
            "__VIEWSTATEGENERATOR":"5E964A8E",
            "ctl00$ContentPlaceHolder1$TextBox2":"",
            "ctl00$ContentPlaceHolder1$search_name":"",
            "domains":"rajyasabha.nic.in",
            "q":"",
            "sitesearch":"rajyasabha.nic.in",
            "ctl00$ContentPlaceHolder1$RadioButtonList1": "Al"
        }

        for row in all_rows[1:]:
            member_link = row.css("td > font > a::attr(id)").extract_first().replace("_","$")
            member_term_from = row.css("td")[4].css("::text").extract_first()
            member_term_to = row.css("td")[5].css("::text").extract_first()
            list_req_params["__EVENTTARGET"] = member_link
            yield scrapy.FormRequest(
                url = "https://rajyasabha.nic.in/rsnew/member_site/MemlistElDate.aspx",
                formdata=list_req_params, 
                callback=self.parse_profile, 
                dont_filter=True,
                meta={
                    'term_from': member_term_from,
                    'term_to': member_term_to
                },
                method="POST"
            )
       
        
    def parse_profile(self, response):
        RSID = response.css("img#ctl00_ContentPlaceHolder1_GridView1_ctl02_Image1").css("::attr(src)").extract_first().split("/")[1].replace("P", "").replace(".jpg", "")
        name = response.css("span#ctl00_ContentPlaceHolder1_GridView1_ctl02_Label3").css("::text").extract_first().strip()
        geography = response.css("table#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_DetailsView1").css("tr")[0].css("td")[1].css("::text").extract_first().strip()
        party = response.css("table#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_DetailsView1").css("tr")[1].css("td")[1].css("::text").extract_first().strip()
        dob = response.css("span#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label14").css("::text").extract_first().strip()
        birth_place = response.css("span#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label15").css("::text").extract_first().strip()
        marital_status = response.css("span#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label1").css("::text").extract_first().strip()
        children = response.css("span#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label2").css("::text").extract_first().strip()
        education = response.css("span#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label16").css("::text").extract_first().strip()
        profession  = response.css("span#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label17").css("::text").extract_first().strip()
        phoneRaw = response.css("span#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label18").css("::text").extract_first().strip()
        phone = re.findall("[0-9]{11}|[0-9]{10}", phoneRaw)
        emailRaw = response.css("img#ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_DetailsView1_Image21").css("::attr(src)").extract_first().split("=")[1].lower().replace(" ", "").replace("email", "").replace(":", "")
        email = emailRaw.split(";") if emailRaw != "" else list()
        yield RSMembers(
            RSID = int(RSID),
            name = name,
            term = {
                'geography': geography,
                'party': party,
                'from': response.meta['term_from'],
                'to': response.meta['term_to'],
                'house': 2,
                'session': None
            },
            dob = dob if dob != '-' else None,
            birth_place = birth_place if birth_place != '-' else None,
            marital_status = marital_status if marital_status != '-'  else None,
            children = children if children != '-'  else None,
            education = education if education != '' else None,
            profession = profession if profession != '' else None,
            phone = phone if len(phone) != 0 else [],
            email = email
        )