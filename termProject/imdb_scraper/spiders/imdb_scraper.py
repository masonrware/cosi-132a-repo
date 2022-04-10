#!usr/bin/python3.9

# scrapy.py
# Version 1.5.0
# 4/9/2022

# Written by: Mason Ware


## This is a python script to scrape imdb for movie reviews and generate a
## csv file of the acquired data.


import scrapy                                   #type: ignore
from imdb_scraper.items import ImdbItem
from scrapy.crawler import CrawlerProcess       #type: ignore

class ImdbSpider(scrapy.Spider):
    ''' This is a web scraper. '''
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start_urls = ('https://www.imdb.com/chart/top')
    
    custom_settings = { 'FEED_FORMAT': 'csv', 'FEED_URI': 'data/IMDB.csv' }
    
    # def start_requests(self):
    #     # The default implementation generaes Request(url, dont_filter = True) for each url in start_urls
        
    def parse(self, response):
        ''' get all html from main imdb page. '''
        for href in response.css("td.titleColumn a::atrr(href)").getall():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_movie)
            
    def parse_movie(self, response):
        ''' get the data from an individual movie page. '''
        item = ImdbItem()
        item['title'] = [x.replace('\xa0', '') for x in response.css(".title-wrapper h1::text").getall()][0]
        item['director'] = response.xpath('//div[@class="creddit_summary_item"]/h4[contain(., "Director")]/following-sibling::a/text()').getall()
        item['writers'] = response.xpath('//div[@class="creddit_summary_item"]/h4[contains(., "Writers")]/following-sibiling::a/text()').getall()
        item['starts'] = response.xpath('//div[@class="creddit_summary_item"]/h4[contains(., "Stars")]/following-sibiling::a/text()').getall()
        item['popularity'] = response.xpath('.titleReviewBarSubItem span.subText::text')[2].re('([0-9]+)')
        item['rating'] = response.css('.ratingValue span::text').get()
        
        return item
    
process = CrawlerProcess()
process.crawl(ImdbSpider)
process.start()  # the script will block here until the cralwing is finished