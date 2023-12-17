# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TravelItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    ticket_ID = scrapy.Field()
    price_old = scrapy.Field() 
    price = scrapy.Field()
    description = scrapy.Field()

    departure_place = scrapy.Field()
    duration = scrapy.Field()
    vehicle = scrapy.Field()
    time_depart = scrapy.Field()

    services = scrapy.Field()
    highlights = scrapy.Field()
    tour_des = scrapy.Field()
    adult_price = scrapy.Field()
    chidren_price = scrapy.Field()
    baby_price = scrapy.Field()

    service_des = scrapy.Field()

class BlogItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
