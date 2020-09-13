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