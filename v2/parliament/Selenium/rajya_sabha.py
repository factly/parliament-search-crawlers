from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
import pymongo
import requests
import shutil

config_file = open("../config.cfg")
config = json.load(config_file)
client = pymongo.MongoClient(config["mongodb_uri"])
db = client["factly_parliament_search"]
collection = db["rajya_sabha_members"]
driver = webdriver.Chrome()
driver.get("https://rajyasabha.nic.in/rsnew/member_site/memberlist.aspx")
assert "Rajya" in driver.title
html_doc = driver.page_source
soup = BeautifulSoup(html_doc, 'html.parser')
list_of_names = soup.find(id="ctl00_ContentPlaceHolder1_GridView2").find_all("a")
for name in list_of_names[136:]:
    driver.get("https://rajyasabha.nic.in/rsnew/member_site/memberlist.aspx")
    assert "Rajya" in driver.title
    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, 'html.parser')
    id = name['id']
    elem = driver.find_element_by_id(id)
    elem.click()
    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, 'html.parser')
    # if collection.find_one({"_id":id}):
    #     continue
    member_details = {
        "_id": id,
        "name":' '.join(soup.find(id='ctl00_ContentPlaceHolder1_GridView1_ctl02_Label3').text.split()),
        "state":soup.find_all('tbody')[1].find_all("tr")[0].find_all("td")[-1].text.strip(),
        "party":soup.find_all('tbody')[1].find_all("tr")[1].find_all("td")[-1].text.strip(),
        "delhi_address":soup.find_all('tbody')[1].find_all("tr")[2].find_all("td")[-1].text.strip(),
        "delhi_phone":soup.find_all('tbody')[1].find_all("tr")[3].find_all("td")[-1].text.strip(),
        "permanent_address":soup.find_all('tbody')[1].find_all("tr")[4].find_all("td")[-1].text.strip(),
        "permanent_phone":soup.find_all('tbody')[1].find_all("tr")[5].find_all("td")[-1].text.strip()
    }
    image_url = "https://rajyasabha.nic.in/rsnew/member_site/photos/"+soup.find(id="ctl00_ContentPlaceHolder1_GridView1_ctl02_Image1")['src'].split("/")[-1]
    response = requests.get(image_url, stream=True, verify=False)
    with open('image/'+id+".jpg", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    #fetch member details
    for bio_row in soup.find(id="ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2").find_all("tr"):
        if bio_row.find("strong"):
            if bio_row.find("strong").text == "Mother's Name\xa0 :\xa0 ":
                member_details["mother"] = bio_row.find("span").text.strip()
            elif bio_row.find_all("strong")[-1].text == "Father's Name\xa0 :\xa0 ":
                member_details["father"] = bio_row.find_all("span")[-1].text.strip()
            elif bio_row.find("strong").text == 'Date of Birth\xa0 :\xa0 ':
                member_details["dob"] = bio_row.find("span").text.strip()
            elif bio_row.find("strong").text == 'Marital Status\xa0 :\xa0 ':
                member_details['marital_status'] = bio_row.find("span").text.strip()
            elif bio_row.find("strong").text == "Spouse's Name\xa0 :\xa0 ":
                member_details['spouse_name'] = bio_row.find("span").text.strip()
            elif bio_row.find("strong").text == 'Children\xa0 \xa0:\xa0 \xa0':
                member_details['children'] = " ".join(bio_row.find("span").text.split())
            elif bio_row.find("strong").text == 'Educational Qualification':
                member_details['education'] = " ".join(bio_row.find(id="ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_DetailsView2_Label16").text.split())
            elif bio_row.find("strong").text == 'Profession :':
                member_details['profession'] = " ".join(bio_row.find_all("span")[-1].text.split())
            elif bio_row.find("strong").text == 'Permanent Address:':
                member_details['present_address'] = " ".join(bio_row.find_all("span")[-1].text.split())
            elif bio_row.find("strong").text == 'Present Address :':
                member_details['present_address'] = " ".join(bio_row.find_all("span")[-1].text.split())
        elif bio_row.find("td",attrs={"style":"font-weight:bold;"}):
            if "Place of Birth" in bio_row.find("td",attrs={"style":"font-weight:bold;"}).text:
                member_details["place_of_birth"] =bio_row.find("td",attrs={"style":"font-weight:bold;"}).text.split("Place of Birth\xa0 :")[1].strip()

    #questions page
    elem = driver.find_element_by_id("__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3")
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_id("__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1")
    elem.click()
    time.sleep(1)
    elem = driver.find_element_by_id("__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3")
    elem.click()
    time.sleep(5)
    html_doc = driver.page_source
    questions = []
    question_soup = BeautifulSoup(html_doc, 'html.parser')
    while question_soup.find("a",string="Next"):
        for question in question_soup.find(id="ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3_GridView2").find_all("tr")[3:-2]:
            question_details = {}
            question_details["number"] = question.find_all("td")[0].text.strip()
            question_details["starred"] = question.find_all("td")[1].text.strip()
            question_details["date"] = question.find_all("td")[2].text.strip()
            question_details["ministry"] = question.find_all("td")[3].text.strip()
            question_details["title"] = question.find_all("td")[4].text.strip()
            questions.append(question_details)
        if question_soup.find("a",string="Next"):
            next_elem = driver.find_elements_by_link_text("Next")[0]
            next_elem.click()
            time.sleep(1)
            html_doc = driver.page_source
            question_soup = BeautifulSoup(html_doc, 'html.parser')
        else:
            break
    member_details["questions"] = questions
    # json.dump(member_details,open("member_details_"+name.text+".json","w+"))
    collection.insert_one(member_details)
    time.sleep(1)

    # tabs = {
    #     "biodata":"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2",
    #     "questions":"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel3",
    #     "assurances":"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel5",
    #     "committees":"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel4",
    #     "mentions":"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel6",
    #     "debates":"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel7",
    #     "bills":"__tab_ctl00_ContentPlaceHolder1_TabContainer1_TabPanel8"
    # }
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source

driver.close()