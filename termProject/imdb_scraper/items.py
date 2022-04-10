import scrapy               # type: ignore

class ImdbItem(scrapy.Item):
    ''' A class to represent an individual movie for the ORM. '''
    title = scrapy.Field()
    director_s = scrapy.Field()
    writer_s = scrapy.Field()
    stars = scrapy.Field()
    popularity = scrapy.Field()
    rating = scrapy.Field()
    #!might want one more for reviews
    