virtualenv venv
cd venv/Scripts
call ./activate
cd ../..
pip install -r requirements.txt
cd parliament
scrapy crawl ls_current_questions_crawler