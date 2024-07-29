import json

with open("person.json") as f:
    json_data = json.load(f)
    print(json_data)