import json
from bs4 import BeautifulSoup

with open('./all_members.html', 'r', encoding='utf-8') as f:
    members = BeautifulSoup(f, 'html.parser')

membersBody = members.find("tbody")
membersRow = membersBody.find_all("tr")

allMembers = list()

for each in membersRow:
    allTD = each.find_all("td")
    MIDlink = allTD[1].find('a', href=True).get('href').split("?")[1]

    MID = MIDlink.split("&")[0].split("=")[1]
    name = allTD[1].find('a', href=True).text.strip()
    party = allTD[2].text.strip()
    constituency = allTD[3].text.strip()
    terms = allTD[4].text.strip().split(',')

    temp = dict()
    temp['MID'] = MID
    temp['name'] = name
    temp['party'] = party
    temp['constituency'] = constituency
    temp['terms'] = terms

    allMembers.append(temp)


allMembers = sorted(allMembers, key = lambda i: i['MID'])

with open('./all_members.json', 'w', encoding='utf-8') as f:
    json.dump(allMembers, f, ensure_ascii=False, indent=4)

    