#!usr/bin/python3

# utils.py
# Version 2.0.0
# 4/10/22

# Written By: Mason Ware


import gzip
import json
import os
from typing import Dict, Generator, Iterable, List, Set
import requests                                                 # type: ignore 
import pandas as pd                                             # type: ignore 
import csv
from collections import namedtuple

from animate import Loader

from dotenv import load_dotenv                                  # type: ignore
from pynytimes import NYTAPI                                    # type: ignore 
from googletrans import Translator                              # type: ignore 


# TODO

# do dupes as well for elastic search

class Commit:
    ''' A class to generate the final json data. It will generate a json file of movies containing all of
        their reviews from 4 sources.'''

    def __init__(self, md_df: "pd.DataFrame", mdb_df: "pd.DataFrame", nyt_df: "pd.DataFrame", tmdb_df: "pd.DataFrame",) -> None:
        self.md_df = md_df
        self.mdb_df = mdb_df
        self.nyt_df = nyt_df
        self.tmdb_df = tmdb_df
        self.movies_set: Set
        self.movies_list: List
      
    def load_data(self) -> None:
        ''' get all movie names in a set and list. '''
        # using movies_metadata.csv because it is by far the largest
        self.movies_set = set(self.md_df['original_title'].tolist())
        self.movies_list = (self.md_df['original_title'].tolist())
        
        
    def generate_movie_json(self) -> Generator[Dict, None, None]:
        ''' generator method to yield a json object of an individual movie and all of its reviews
            to be written to a file with unique movies. '''
        translator = Translator()
        loader = Loader("Compressing Unique Movie Data...", "All done!", 0.05).start()
        for title in self.movies_set:
            result = translator.translate(title)
            if result and result.src == 'en':
                # TODO
                # find more relevant, persistent data
                # add more keys below
                # get popularity scores
                json_obj = dict.fromkeys(['title', 'reviews', 'popularity'])
                json_obj['reviews'] = []
                json_obj['title'] = title
                # find all in movies_metadata.csv
                for index, row in md_df.iterrows():
                    if row['original_title'].lower() == title.lower():
                        movie_data = {
                            'review': row['overview'],
                            'src': 'movies_metadata'
                        }
                        json_obj['reviews'].append(movie_data)
                # find all in mdblist
                for index, row in mdb_df.iterrows():
                    if row['title'].lower() == title.lower():
                        movie_data = {
                            'review': row['description'],
                            'src': 'mdblist'
                        }
                        json_obj['reviews'].append(movie_data)
                # find all in nyt
                for index, row in nyt_df.iterrows():
                    if row['display_title'].lower() == title.lower():
                        movie_data = {
                            'review': row['summary_short'],
                            'src': 'nyt'
                        }
                        json_obj['reviews'].append(movie_data)  
                # find all in tmdb
                for index, row in tmdb_df.iterrows():
                    for movie in row['results']:
                        if movie['original_title'].lower() == title.lower():
                            movie_data = {
                                'review': movie['overview'],
                                'src': 'tmdb'
                            }
                            json_obj['reviews'].append(movie_data)
                            
                json_obj['reviews'] = [dict(t) for t in {tuple(d.items()) for d in json_obj['reviews']}]
                yield json_obj
        loader.stop()
        
    def generate_dupe_movie_json(self) -> Generator[Dict, None, None]:
        ''' generator method to yield a json object of an individual movie and review
            to be written to a file with duplicated movies. '''
        translator = Translator()
        loader = Loader("Compressing Duplicate Movie Data...", "All done!", 0.05).start()

        for title in self.movies_list:
            result = translator.translate(title)
            if result and result.src == 'en':
                json_obj = dict.fromkeys(['title', 'review', 'popularity'])
                json_obj['title'] = title
                # only need to look in movie_metdata.csv because that is where we started from
                for index, row in md_df.iterrows():
                    if row['original_title'].lower() == title.lower():
                        json_obj['review'] = row['overview']
            yield json_obj
        loader.stop()
        
    def write_unique(self, json_objs: Iterable, target_file: str) -> None:
        ''' write a json_obj of a unique movie to a target file. '''
        # ensure that the movie has multiple reviews and that they are unique
        for json_obj in json_objs:
            if len(json_obj['reviews'])>1:           
                # convert into JSON string
                json_str = json.dumps(json_obj, indent=4, sort_keys=True)
                with open(target_file, 'a') as outfile:
                    outfile.write(json_str)
                    outfile.write(',')
    
    def write_dupe(self, json_objs: Iterable, target_file: str) -> None:
        ''' wrtie a json_obj of a duplicated movie to a target file. '''
        for json_obj in json_objs:
            json_str = json.dumps(json_obj, indent=4, sort_keys=True)
            with open(target_file, 'a') as outfile:
                outfile.write(json_str)
                outfile.write(',')

class API:
    ''' A class to execute one or many api calls and generate .json files with their output. '''
    def __init__(self) -> None:
        load_dotenv()
        # work in data subdir
        os.chdir('../data/')
    
    def nyt_api(self, in_file_path: str, out_file_path: str) -> None:
        # check to make nyt calls
        # write to data/nyt.json
        if not os.path.exists('nyt.json'):
            nyt = NYTAPI(os.getenv('API_KEY'), parse_dates=True)
            reviews = nyt.movie_reviews
            url = 'https://api.nytimes.com/svc/movies/v2/reviews/all.json?api-key=' + os.getenv('API_KEY')
            json_str = json.dumps(requests.get(url).json(), indent=4, sort_keys=True)

            loader = Loader("Writing nyt data to data/nyt.json...", "All done!", 0.05).start()
            # write first page
            with open(out_file_path, 'w') as outfile:
                outfile.write(json_str)
                
            # write the rest
            with open(in_file_path, 'r') as file:
                json_data = json.load(file)
            json_str = json.dumps(json_data, indent=4, sort_keys=True)
            with open(out_file_path, 'w') as outfile:
                outfile.write(json_str)
            loader.stop()

    def tmdb_api(self, url: str, out_file_path: str) -> None:
        # check to make tmdb calls
        # write to data/tmdb_raw.json
        # this call will return all movies in all languages as of april 21st, 2022
        if not os.path.exists('tmdb_raw.json'):
            import zlib
            import urllib

            f=urllib.request.urlopen(url) 
            decompressed_data=zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
            with open(out_file_path, 'wb') as f:
                f.write(decompressed_data)
        # check to find english tmdb entries and get full json image
        # write to data/tmdb.json
        elif os.path.exists('tmdb_raw.json') and not os.path.exists('tmdb.json'):
            translator = Translator()
            out_file_path = '/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb.json'
            
            from animate import Loader
            loader = Loader("Writing tmdb english data to data/tmdb.json...", "All done!", 0.05).start()
            
            with open('/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb_raw.json') as movies:
                for movie in movies:
                    json_dict = json.loads(movie)
                    title = json_dict['original_title']
                    if title:
                        # get all english movies only
                        result = translator.translate(title)
                        if result and result.src == 'en':
                            url = f'https://api.themoviedb.org/3/search/movie?api_key=dae980beb03de6af72723c0778acdc0e&query=' + ('+').join(title.split(' '))
                            response = requests.get(url)
                            if response.status_code==200:
                                json_str = json.dumps(response.json(), indent=4, sort_keys=True)
                                with open(out_file_path, 'a') as outfile:
                                    outfile.write(json_str)
            loader.stop()  

    def mdblist_api(self, mdblist_out_file_path: str, tmdb_in_file_path: str) -> None:
        if not os.path.exists('mdblist.json'):
            loader = Loader("Writing mdblist data to data/mdblist.json...", "All done!", 0.05).start()
                
            with open(tmdb_in_file_path) as movies:
                dict1 = json.load(movies)
                for page in dict1:
                    for movie in page['results']:
                        title = movie['original_title'].lower()
                        url = f'https://mdblist.com/api/?apikey=cvd24hv7j9t955qygrrlgvmxj&s=' + ('+').join(title.split(' '))
                        response = requests.get(url)
                        if response.status_code==200:
                            for item in response.json()['search']:
                                imdbid = (item['imdbid'])
                                if imdbid:
                                    url = 'https://mdblist.com/api/?apikey=cvd24hv7j9t955qygrrlgvmxj&i=' + imdbid
                                    response = requests.get(url)
                                    if response.status_code==200:
                                        json_str = json.dumps(response.json(), indent=4, sort_keys=True)
                                        with open(mdblist_out_file_path, 'a') as outfile:
                                            outfile.write(json_str)          
                
            loader.stop()
    

if __name__=='__main__':
    unique_target_file = '/Users/masonware/Desktop/COSI_132A/termProject/data/final_unique_movie_data.json'
    duplicated_target_file = '/Users/masonware/Desktop/COSI_132A/termProject/data/final_dupe_movie_data.json'
    
    # TODO
    # add args options to:
    # 1.  commit dupe data
    # 2.  commit unique data
    # 3.  make all api calls
    # 4.    make each api call
    
    # add error handeling for making commits before making calls
    
    
    md = '/Users/masonware/Desktop/COSI_132A/termProject/data/movies_metadata.csv'
    mdb = '/Users/masonware/Desktop/COSI_132A/termProject/data/mdblist.json'
    nyt = '/Users/masonware/Desktop/COSI_132A/termProject/data/nyt.json'
    tmdb = '/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb.json'
    nyt_in_file_path = 'termProject/data/reviews.json'  # deprecated
    tmdb_url = 'http://files.tmdb.org/p/exports/movie_ids_04_21_2022.json.gz'
    tmdb_out_file_path = '/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb_raw.json'
    
    # move below to a function and that way I can try catch with the call to see if there is a file or not - if not please make api call
    md_df = pd.read_csv(md, low_memory=False)
    mdb_df = pd.read_json(mdb)
    nyt_df = pd.read_json(nyt)
    tmdb_df = pd.read_json(tmdb)
    
    commit = Commit(md_df=md_df,
                    mdb_df=mdb_df,
                    nyt_df=nyt_df,
                    tmdb_df=tmdb_df)
    
    apis = API()
    
    apis.nyt_api(in_file_path=nyt_in_file_path, out_file_path=nyt)
    apis.tmdb_api(url=tmdb_url, out_file_path=tmdb_out_file_path)
    apis.mdblist_api(mdblist_out_file_path=mdb, tmdb_in_file_path=tmdb_out_file_path)
    # add class creation for api calls
    
    
    commit.load_data()
    commit.write_unique(commit.generate_movie_json(), unique_target_file) 
    


