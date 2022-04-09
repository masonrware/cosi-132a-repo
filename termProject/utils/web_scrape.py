#!usr/bin/python3.9

# web_scrape.py
# Version 1.0.0
# 4/9/2022

# Written by: Mason Ware


## This is a python script to scrape imdb for movie reviews and generate a
## csv file of the acquired data.


import scrapy       #type: ignore


class MovieItem(scrapy.Item):
    ''' A class to represent an individual movie for the ORM. '''
    title = scrapy.Field()
    director_s = scrapy.Field()
    writer_s = scrapy.Field()
    stars = scrapy.Field()
    popularity = scrapy.Field()
    #!might want one more for reviews
    

class Spider(scrapy.Spider):
    ''' This is a web scraper. '''
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ('https://www.imdb.com/boxoffice/',)
    
    