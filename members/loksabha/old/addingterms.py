import json

with open('./withcleanname.json', 'r', encoding='utf-8') as f:
    members = json.load(f)

with open('./termswithcleanname.json', 'r', encoding='utf-8') as f:
    sessions = json.load(f)

with open('./sessiondate.json', 'r', encoding='utf-8') as f:
    times = json.load(f)

newMembers = list()

for member in members:
    name = member['name']
    terms = member['terms']
    newTerms = list()

    if len(terms) == 1:
        tempTerm = dict()
        tempTerm['house'] = 1
        tempTerm['constituency'] = member['constituency']
        tempTerm['party'] = member['party']
        tempTerm['session'] = int(terms[0])
        tempTerm['from'] = times[terms[0]]['from']
        tempTerm['to'] = times[terms[0]]['to']

        newTerms.append(tempTerm)
    else:
        for term in terms:

            sessionTermDetails = list(filter(lambda person: person['name'] == name, sessions[term]))
            if len(sessionTermDetails) == 1:
                termDetails = sessionTermDetails[0]
                tempTerm = dict()
                tempTerm['house'] = 1
                tempTerm['constituency'] = termDetails['constituency']
                tempTerm['party'] = termDetails['party']
                tempTerm['session'] = int(term)
                tempTerm['from'] = times[term]['from']
                tempTerm['to'] = times[term]['to']
                
                newTerms.append(tempTerm)
            else:
                print(name)
                print(terms)


    member['terms'] = newTerms

    newMembers.append(member)

with open('./withterms.json', 'w', encoding='utf-8') as f:
    json.dump(newMembers, f, ensure_ascii=False, indent=4)

