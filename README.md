# parliament-search-crawlers

This repo contains the code to crawl over Lok Sabha, Rajya Sabha websites, persist the data into database and ensure data quality/consistency.

This repo contains 8 spiders

1. ls_party
2. rs_party
3. ministries
4. ls_current_members
5. rs_current_members
6. ls_questions
7. ls_questions_by_date
8. rs_questions

## 1. ls_party

This spider crawls all political parties of current lok sabha members

### How to run

    scrapy crawl ls_party -o ls_party.json

### Type of error log

1. { "type": "ministry not found", ...}
   This means ministry name is not present in './data/ministries.json'
2. { "type": "\${X} match for question by", ...}
   This means for crawler is not able to single member with same name.
3. { "type": "ERROR", ...}
   When something goes wrong with network request

### Post run

1. Check the errors.log based on error take action

## 2. rs_party

This spider crawls all political parties of current rajya sabha members

### How to run

    scrapy crawl rs_party -o rs_party.json

### Type of error log

1. { "type": "ministry not found", ...}
   This means ministry name is not present in './data/ministries.json'
2. { "type": "\${X} match for question by", ...}
   This means for crawler is not able to single member with same name.
3. { "type": "ERROR", ...}
   When something goes wrong with network request

### Post run

Check the errors.log and take actions based on that
Example - If you see ministry not found then either create new ministry if required or use already existing ministry ID with same role

## 3. ministries

This spider crawls all Ministry in given lok sabha session

### Input

1. session

### How to run

    scrapy crawl ministries -a session=17 -o session_ministries.json

### Type of error log

1. {'name': 'ROAD TRANSPORT AND HIGHWAYS'}
   2020-09-30 07:23:37 [scrapy.core.scraper] WARNING: Dropped: already_there
   This means ministry with same name is already there in database

## 4. ls_current_members

This spider crawls current member of lok sabha

### Pre-run

Before running this crawler change `session` variable in `ls_current_members.py` file

### How to run

scrapy crawl ls_current_members -o ls_members.json

### Type of error log

1. { 'message': "geography not found"}
   This means crawler didn’t find geography name in db
2. { 'message': "party not found" }
   This means crawler didn’t find party name in db

## 5. rs_current_members

This spider crawls current members of rajya sabha

### How to run

    scrapy crawl rs_current_members -o rs_members.json

### Type of error log

1. { 'message': "geography not found"}
   This means crawler didn’t find geography name in db
2. { 'message': "party not found" }
   This means crawler didn’t find party name in db

### Post run

Check the errors.log and take actions based on that
Example - If you see geography not found then either create new geography if required or use already existing geography ID with same role

## 6. ls_questions

This spider crawls all the questions in given lok sabha session

### Input

1. session

### How to run

    scrapy crawl ls_questions -a session=17 -o session_questions.json

## 7. ls_questions_by_date

This spider crawls all the questions in given lok sabha session and time frame

### Input

1. session
2. from_date
3. to_date

### How to run

    scrapy crawl ls_questions_by_date -a session=17 -a from_date=25.06.2019 -a to_date=19.03.2020 -o session_questions.json

## 8. rs_questions

This spider crawls all the questions in given rajya sabha session and question type

### Input

1. session
2. qtype(0=STARRED, 1=UNSTARRED)

### How to run

    scrapy crawl rs_questions -a session=242 -a qtype=1 -o session_qtype_questions.json
