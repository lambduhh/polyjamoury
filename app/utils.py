import json


def open_json_data(data):
    with open('data.json', 'w') as f: f.write(json.dumps(data, indent=2))
