import json

with open('./crawlers/q17.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions = sorted(questions, key = lambda i: int(i['qref'].split("_")[1]))


newQuestions = list()
start = 1000000
for each in questions:
    each['QID'] = start
    start += 1
    newQuestions.append(each)


with open('q17_with_ID_2.json', 'w', encoding='utf-8') as f:
    json.dump(newQuestions, f, ensure_ascii=False, indent=4)