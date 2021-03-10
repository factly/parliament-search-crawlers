# parliament-search-crawlers
This repo contains the code to crawl over Lok Sabha, Rajya Sabha websites, persist the data into database and ensure data quality/consistency.

This repo contains 8 spiders
1. ls_current_members
2. ls_party
3. ls_questions_by_date
4. ls_questions
5. ministries
6. rs_current_members
7. rs_party
8. rs_questions

## ls_party
This spider crawls all political parties of current lok sabha members

How to run

    scrapy crawl ls_party -o ls_party.json
    
## rs_party
This spider crawls all political parties of current rajya sabha members

How to run

    scrapy crawl ls_party -o rs_party.json

## ministries
This spider crawls all Ministry in given lok sabha session

Input
1. session

How to run

    scrapy crawl ministries -a session=17 -o session_ministries.json

## ls_current_members
This spider crawls current member of lok sabha

Before running this crawler change `session` variable in `ls_current_members.py` file

How to run

    scrapy crawl ls_current_members -o ls_members.json

## rs_current_members
This spider crawls current members of rajya sabha

How to run

    scrapy crawl rs_current_members -o rs_members.json

## ls_questions
This spider crawls all the questions in given lok sabha session

Input
1. session

How to run

    scrapy crawl ls_questions -a session=17 -o session_questions.json

## ls_questions_by_date
This spider crawls all the questions in given lok sabha session and time frame

Input
1. session
2. from_date
3. to_date

How to run

    scrapy crawl ls_questions -a session=17 -a from_date=25.06.2019 -a to_date=19.03.2020 -o session_questions.json

## rs_questions
This spider crawls all the questions in given rajya sabha session and question type

Input
1. session
2. qtype(0=STARRED, 1=UNSTARRED)

How to run

    scrapy crawl rs_questions -a session=242 -a qtype=1 -o session_qtype_questions.json


## Functional Know How on the Parlens Project

Parlens project's aim is to get the data from Loksabha and Rajyasabha website to be collected, cleaned and put in a very structured format for usage by Parlens tool.

Currently the data is in google shared folder by name parlens mongo owned by shashi and shared with somitra.

Data that is present in both Loksabha and Rajyasabha are as below:
1. Ministries

        {
        "_id": {
            "$oid": "5e00b12a4c6f42d85c839d4e"
        },
        "MINID": 1001,
        "name": "HEALTH AND FAMILY WELFARE"
        }

2. Parties

        {
        "_id": {
            "$oid": "5e258ce692f43f8fa7d3ad9a"
        },
        "PID": 1,
        "name": "Aam Aadmi Party",
        "abbr": "AAP"
        }

3. Geographies

        {
        "_id": {
            "$oid": "5e254cb0a783d6d2a9869f79"
        },
        "GID": 1000,
        "name": "India",
        "type": "country",
        "parent": 1000,
        "category": "GEN"
        }

4. Members

        {
        "_id": {
            "$oid": "5e43a0e52499593e59d5b456"
        },
        "MID": 10000,
        "name": "Prasanna Acharya",
        "terms": [
            {
            "house": 1,
            "geography": 1104,
            "party": 29,
            "session": 12,
            "from": 889468200000,
            "to": 925065000000
            },
            {
            "house": 1,
            "geography": 1104,
            "party": 29,
            "session": 13,
            "from": 939493800000,
            "to": 1076005800000
            },
            {
            "house": 1,
            "geography": 1104,
            "party": 29,
            "session": 14,
            "from": 1084732200000,
            "to": 1242585000000
            },
            {
            "house": 2,
            "session": null,
            "geography": 1026,
            "party": 29,
            "from": 1467397800000,
            "to": 1656613800000
            }
        ],
        "birthPlace": "Bargarh (Orissa)",
        "prefix": "Shri",
        "fullName": "Shri Prasanna Acharya",
        "dob": -643786200000,
        "maritalStatus": 1,
        "sons": null,
        "daughters": 2,
        "education": 3,
        "gender": 2,
        "email": [],
        "phone": [],
        "LSID": 5,
        "RSID": 2341
        }
5. Questions

        {
        "_id": {
            "$oid": "5e43c78759482908d2742d65"
        },
        "qref": "17_1",
        "house": 1,
        "ministry": 1001,
        "date": "2019-06-21",
        "subject": "Empanellment of Hospitals under PMSSY",
        "question": "<td class=\"stylefontsize\">\r\n                                                    Will the Minister of HEALTH AND FAMILY WELFARE be pleased to state: <br><br>(a) whether hospitals have been empanelled to provide treatment under the Pradhan Mantri Swasthya Suraksha Yojana (PMSSY) in Bihar; <br><br>(b) if so, the details thereof; <br><br>(c) whether funds have been allocated under this scheme in Bihar; <br><br>(d) if so, the details thereof, till date; and <br><br>(e) whether the Government has given discretionary quota for the public representative in this regard, if so, the details thereof?<br>\r\n                                                </td>",
        "answer": "<td class=\"stylefontsize\">\r\n                                                        ANSWER<br>THE MINISTER OF STATE IN THE MINISTRY OF HEALTH AND <br>FAMILY WELFARE<br>(SHRI ASHWINI KUMAR CHOUBEY)<br>(a):    No. The Pradhan Mantri Swasthya Suraksha Yojana (PMSSY) aims at correcting the imbalances in the availability of affordable healthcare facilities in different parts of the country in general, and augmenting facilities for quality medical education in the under-served States in particular.  PMSSY, a Central Sector Scheme has two components-setting up of AIIMS-like Institutions and upgradation of existing State Government Medical College/Institutions in a phased manner.  <br>Therefore, as such there is no provision of empanelment of hospitals to provide treatment under the Pradhan Mantri Swasthya Suraksha Yojana (PMSSY).<br>(b):    Does not arise.<br>(c) &amp; (d):   Under PMSSY, AIIMS Patna has already become functional and another AIIMS has been announced in the State of Bihar. <br>Apart from this, Six (6) existing Government Medical Colleges in Bihar have been taken up for up-gradation by creation of Super Speciality Blocks (SSB).  Details of projects taken up under PMSSY and fund released under these Projects is given in  Annexure.<br>(e):      No.<br>…………..<br>\r\n                                                    </td>",
        "questionBy": [
            13905
        ],
        "hindiPdf": "http://164.100.24.220\\loksabhaquestions\\qhindi\\171\\AU2.pdf",
        "englishPdf": "http://164.100.24.220\\loksabhaquestions\\annex\\171\\AU2.pdf",
        "type": "UNSTARRED",
        "QID": 1000000
        }

6. Houses, Education Level, Gender Category, Marital Status

If we carefully look at the JSON data of members above, this member details are linked to other collections through the member id - MID is linked to Questions with field questionBy

Terms in Members data will have the details of the houses that particular member has served in along with start and end period for both rajyasabha and loksabha. There are many cases where one minister is part of loksabha and rajyasabha as well, identified by LSID and RSID to map to questions asked in both loksabha and rajyasabha

Other JSONs hold the master data on houses, education level, marital status, gender, geography and they are linked by their respective IDs wherever they popup in Members data.

Data retrieved by the spiders are processed through a series of pipelines to clean and structurise the data. The information present on the Loksabha and rajyasabha

        'parlens.pipelines.lsmembers.DuplicateCleaner': 5, # remove already existing member based on LSID
        'parlens.pipelines.members.NameCleaner': 10, # seprate name and prefix 
        'parlens.pipelines.members.EducationCleaner': 20, # clean education field and assign value
        'parlens.pipelines.members.MaritalCleaner': 30, # clean marital field and assign appropriate value
        'parlens.pipelines.members.ProfessionCleaner': 40, # clean profession 
        'parlens.pipelines.lsmembers.DOBCleaner': 50, # convert dob into timestamp
        'parlens.pipelines.lsmembers.EmailCleaner': 60, # clean email field
        'parlens.pipelines.lsmembers.ChildrenCleaner': 70, # clean sons and daughters field
        'parlens.pipelines.lsmembers.GeoTermCleaner': 80, # convert geography field into GID  
        'parlens.pipelines.lsmembers.PartyTermCleaner': 90, # convert party field into PID
        'parlens.pipelines.lsmembers.TermConstructor': 100, # Construct term object and remove party and geography field

The logic for each of the spiders and respective pipelines vary depending on how the data is present on the website and is to be cleaned. Please look into the pipeline functions to get a more detailed understanding of the pipelines.

## Next Steps

We need to get the data for all the questions from Loksabha and Rajyasabha. We can do that by running ls_questions_by_date and rs_questions spiders. You can see the documentation above on how to run it.

Running these scrapers will give us json files, we need to add these data into all_questions.json file which is on the google drive or add them to the MongoDB instance which has all the data using python script uploader.py in this repo. 

Note: You will have to do it for each files that we generate for both rajyasabha and loksabha.

We would also need to get the latest information on the members in both loksabha and rajyasabha, could have changed since the time we ran the scraper last.