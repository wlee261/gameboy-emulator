import json

with open('opcodes.json','r') as file:
    json_data = json.load(file)

for line in json_data.items():
    print(line,'\n')