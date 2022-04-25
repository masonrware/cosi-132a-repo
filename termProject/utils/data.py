#!usr/bin/python3

# utils.py
# Version 2.0.0
# 4/10/22

# Written By: Mason Ware


import gzip
import json
import os
import requests                     # type: ignore 

from animate import Loader

from dotenv import load_dotenv      # type: ignore
from pynytimes import NYTAPI        # type: ignore 
from googletrans import Translator





# TODO

# make a .jl file for every movie
# get all movies into a nondupe .jl file

import pandas as pd
import csv

md = '/Users/masonware/Desktop/COSI_132A/termProject/data/movies_metadata.csv'
mdb = '/Users/masonware/Desktop/COSI_132A/termProject/data/mdblist.json'
nyt = '/Users/masonware/Desktop/COSI_132A/termProject/data/nyt.json'
tmdb = '/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb.json'
md_df = pd.read_csv(md, low_memory=False)
mdb_df = pd.read_json(mdb)
nyt_df = pd.read_json(nyt)
tmdb_df = pd.read_json(tmdb)



# print(tmdb_df.head())

movies_set = set(md_df['original_title'].tolist())
movies_list = (md_df['original_title'].tolist())

translator = Translator()

# # for dupes
# for title in movies_list:
#     line = {}
#     result = translator.translate(title)
#     if result and result.src == 'en':
#         pass
        
        
# for non-dupes  
for title in movies_set:
    result = translator.translate(title)
    if result and result.src == 'en':
        
        # TODO
        # fix below so that it works?
        json_obj = dict()
        json_obj['title'] = title.lower()
        json_obj['reviews'] = list()
        
        
        
        # find all in movies_metadata.csv
        for index, row in md_df.iterrows():
            if row['original_title'].lower() == title.lower():
                json_obj['reviews'].append(row['overview'])
                
        # find all in mdblist
        for index, row in mdb_df.iterrows():
            if row['title'].lower() == title.lower():
                json_obj['reviews'].append(row['description'])
                
        # find all in nyt
        for index, row in nyt_df.iterrows():
            if row['display_title'].lower() == title.lower():
                json_obj['reviews'].append(row['summary_short'])
                
        # # find all in tmdb
        # for index, row in tmdb_df.iterrows():
        #     if row['original_title'].lower() == title.lower():
        #         json_obj['reviews'].append(row['overview'])
                
        with open('/Users/masonware/Desktop/COSI_132A/termProject/data/test.json', 'a') as outfile:
            # print(type(json_obj))
            json.dump(json.dumps(dict(json_obj)), outfile)
        json_obj.clear()
    # print(json_obj if json_obj['title'] else 'NONE')
    # print('\n')
    

    
#################################################
#################################################

  
# load_dotenv()

# # work in data subdir
# os.chdir('../data/')


# # check to make nyt calls
# # write to data/nyt.json
# if not os.path.exists('nyt.json'):
#     out_file_path = '/Users/masonware/Desktop/COSI_132A/termProject/data/nyt.json'
#     in_file_path = 'termProject/data/reviews.json'  # deprecated
#     nyt = NYTAPI(os.getenv('API_KEY'), parse_dates=True)
#     reviews = nyt.movie_reviews
#     url = 'https://api.nytimes.com/svc/movies/v2/reviews/all.json?api-key=' + os.getenv('API_KEY')
#     json_str = json.dumps(requests.get(url).json(), indent=4, sort_keys=True)

#     loader = Loader("Writing nyt data to data/nyt.json...", "All done!", 0.05).start()
#     # write first page
#     with open(out_file_path, 'w') as outfile:
#         outfile.write(json_str)
        
#     # write the rest
#     with open(in_file_path, 'r') as file:
#         json_data = json.load(file)
#     json_str = json.dumps(json_data, indent=4, sort_keys=True)
#     with open(out_file_path, 'w') as outfile:
#         outfile.write(json_str)
#     loader.stop()
    
    
# # check to make tmdb calls
# # write to data/tmdb_raw.json
# # this call will return all movies in all languages as of april 21st, 2022
# if not os.path.exists('tmdb_raw.json'):
#     url = 'http://files.tmdb.org/p/exports/movie_ids_04_21_2022.json.gz'
#     target = '/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb_raw.json'
#     import zlib
#     import urllib

#     f=urllib.request.urlopen(url) 
#     decompressed_data=zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
#     with open(target, 'wb') as f:
#         f.write(decompressed_data)
    
    
# # check to find english tmdb entries and get full json image
# # write to data/tmdb.json
# elif os.path.exists('tmdb_raw.json') and not os.path.exists('tmdb.json'):
#     translator = Translator()
#     out_file_path = '/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb.json'
    
#     from animate import Loader
#     loader = Loader("Writing tmdb english data to data/tmdb.json...", "All done!", 0.05).start()
    
#     with open('/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb_raw.json') as movies:
#         for movie in movies:
#             json_dict = json.loads(movie)
#             title = json_dict['original_title']
#             if title:
#                 # get all english movies only
#                 result = translator.translate(title)
#                 if result and result.src == 'en':
#                     url = f'https://api.themoviedb.org/3/search/movie?api_key=dae980beb03de6af72723c0778acdc0e&query=' + ('+').join(title.split(' '))
#                     response = requests.get(url)
#                     if response.status_code==200:
#                         json_str = json.dumps(response.json(), indent=4, sort_keys=True)
#                         with open(out_file_path, 'a') as outfile:
#                             outfile.write(json_str)
#     loader.stop()  
                    

# if not os.path.exists('mdblist.json'):
#     target = '/Users/masonware/Desktop/COSI_132A/termProject/data/mdblist.json'
#     res = []
    
#     loader = Loader("Writing mdblist data to data/mdblist.json...", "All done!", 0.05).start()
        
#     with open('/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb.json') as movies:
#         dict1 = json.load(movies)
#         for page in dict1:
#             for movie in page['results']:
#                 title = movie['original_title'].lower()
#                 url = f'https://mdblist.com/api/?apikey=cvd24hv7j9t955qygrrlgvmxj&s=' + ('+').join(title.split(' '))
#                 response = requests.get(url)
#                 if response.status_code==200:
#                     for item in response.json()['search']:
#                         imdbid = (item['imdbid'])
#                         if imdbid:
#                             url = 'https://mdblist.com/api/?apikey=cvd24hv7j9t955qygrrlgvmxj&i=' + imdbid
#                             response = requests.get(url)
#                             if response.status_code==200:
#                                 json_str = json.dumps(response.json(), indent=4, sort_keys=True)
#                                 with open(target, 'a') as outfile:
#                                     outfile.write(json_str)          
        
#     loader.stop()