import json

with open('./data/states.json', 'r', encoding='utf-8') as f:
    states = json.load(f)

allStates = list()

for state in states:
    tempState = dict()
    tempState['GID'] = states[state]
    tempState['name'] = state
    tempState['which'] = 'state'
    tempState['parent'] = 1000
    tempState['type'] = 3

    allStates.append(tempState)


with open('./states_list.json', 'w', encoding='utf-8') as f:
    json.dump(allStates, f, ensure_ascii=False, indent=4)