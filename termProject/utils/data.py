#!usr/bin/python3

# utils.py
# Version 2.0.0
# 4/10/22

# Written By: Mason Ware


import gzip
import json
import os
import requests                     # type: ignore 

from dotenv import load_dotenv      # type: ignore

from pynytimes import NYTAPI        # type: ignore 
from googletrans import Translator


load_dotenv()

# work in data subdir
os.chdir('../data/')




# TODO
# 1. work on third api call

# 2. get fourth api call

# 3. write all to json files

# 4. write script to comb all json files for similar movies and make one giant .jl 
# file with their json objects and have it be standardized

# 5. make class for data generation with a method for each function:
#       loading json data
#       creating final data sheet
# ^all of which return booleans so no-crash when building



# check to make nyt calls
# write to data/nyt.json
if not os.path.exists('nyt.json'):
    out_file_path = '/Users/masonware/Desktop/COSI_132A/termProject/data/nyt.json'
    in_file_path = 'termProject/data/reviews.json'  # deprecated
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
    
    
# check to make tmdb calls
# write to data/tmdb_raw.json
# this call will return all movies in all languages as of april 21st, 2022
if not os.path.exists('tmdb_raw.json'):
    url = 'http://files.tmdb.org/p/exports/movie_ids_04_21_2022.json.gz'
    target = '/Users/masonware/Desktop/COSI_132A/termProject/data/tmdb_raw.json'
    import zlib
    import urllib

    f=urllib.request.urlopen(url) 
    decompressed_data=zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
    with open(target, 'wb') as f:
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
                        json_str = json.dumps(requests.get(url).json(), indent=4, sort_keys=True)
                        with open(out_file_path, 'a') as outfile:
                            outfile.write(json_str)
    loader.stop()  
                    
#################################################
#################################################

# TODO
# work out below api calls 
    
'https://mdblist.com/api/?apikey=[apikey]&s=jaws'
 
url = "https://mdblist.p.rapidapi.com/"
querystring = {"i":"tt0073195"}
headers = {
	"X-RapidAPI-Host": "mdblist.p.rapidapi.com",
	"X-RapidAPI-Key": "e7f231b238msh3f4f9bfe360d40bp1dae6ajsn73fa3202855b"
}


response = requests.request("GET", url, headers=headers, params=querystring)
print(response)
if response.status_code==200:
    print(response.text)

#################################################
#################################################