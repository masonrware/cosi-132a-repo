#!usr/bin/python3

# utils.py
# Version 2.0.0
# 4/10/22

# Written By: Mason Ware


## This is a script to interact with the NYT API and retrieve
## movie reviews as json data.


import json
import os
from dotenv import load_dotenv      # type: ignore
import requests                     # type: ignore 

from pynytimes import NYTAPI        # type: ignore 

load_dotenv()


# out_file_path = 'termProject/data/movie_reviews.json'
# in_file_path = 'termProject/data/reviews.json'

# nyt = NYTAPI(os.getenv('API_KEY'), parse_dates=True)
# reviews = nyt.movie_reviews     # get reviews (could do other categories)

# url = 'https://api.nytimes.com/svc/movies/v2/reviews/all.json?api-key=' + os.getenv('API_KEY')
# json_str = json.dumps(requests.get(url).json(), indent=4, sort_keys=True)

# # write retrieved 20
# with open(out_file_path, 'w') as outfile:
#     outfile.write(json_str)
    
# # write the rest
# with open(in_file_path, 'r') as file:
#     json_data = json.load(file)
# json_str = json.dumps(json_data, indent=4, sort_keys=True)
# with open(out_file_path, 'w') as outfile:
#     outfile.write(json_str)
   
#! below link if from forum
 
res = requests.get('http://files.tmdb.org/p/exports/movie_ids_04_21_2022.json.gz')
if res.status_code == 200:
    print(res.text)


# ?
#TODO
# get list of valid movie ids
# iterate over them
# make an individual call for each movie review
# ?


# TODO
# restructure requests so that I am making calls based on movie title!
# make calls to at least 5 apis!

### api urls ###
'https://api.themoviedb.org/3/review/401478?api_key=dae980beb03de6af72723c0778acdc0e'
'https://api.themoviedb.org/3/movie/401478/reviews?api_key=dae980beb03de6af72723c0778acdc0e'
################