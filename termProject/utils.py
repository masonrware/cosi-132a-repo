#!usr/bin/python3

# utils.py
# Version 1.0.0
# 4/10/22

# Written By: Mason Ware

import os
from dotenv import load_dotenv
import json
import datetime
import requests                     # type: ignore 

from pynytimes import NYTAPI        # type: ignore 

load_dotenv()

out_file_path = 'termProject/data/movie_reviews.json'
in_file_path = 'termProject/data/reviews.json'
nyt = NYTAPI(os.getenv('API_KEY'), parse_dates=True)
reviews = nyt.movie_reviews # this isn't working need to serialize

url = 'https://api.nytimes.com/svc/movies/v2/reviews/all.json?api-key=' + os.getenv('API_KEY')
r = requests.get(url)
json_data = r.json()
json_str = json.dumps(json_data, indent=4, sort_keys=True)

with open(out_file_path, 'w') as outfile:
    outfile.write(json_str)
    
with open(in_file_path, 'r') as file:
    json_data = json.load(file)
json_str = json.dumps(json_data, indent=4, sort_keys=True)
with open(out_file_path, 'w') as outfile:
    outfile.write(json_str)

# print(reviews)