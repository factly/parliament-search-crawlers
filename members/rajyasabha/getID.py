from bs4 import BeautifulSoup
import json
with open('./members/rajyasabha/all_members.html', 'r', encoding='utf-8') as f:
    members = BeautifulSoup(f, 'html.parser')

membersBody = members.find("tbody")
membersRow = membersBody.find_all("tr")

final = list()

for member in membersRow[1:]:
    tds = member.find_all("td")
    if( tds[0].text.strip() != ''):
        temp = dict()
        temp['name'] = tds[2].text.strip()
        temp['RSID'] = tds[1].find("img")['src'].split("/")[1].replace("P", "").replace(".jpg", "")
        
        final.append(temp)
        
with open('witha.json', 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=4)