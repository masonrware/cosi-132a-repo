import os
import json

with open ('pa5_data/pa5_queries.json', 'r') as f:
    data = json.load(f)
    for line in data['pa5_queries']:
        print(line['topic'])