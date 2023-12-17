# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DulichItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    ticket_ID = scrapy.Field()
    trip = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()

    departure_place = scrapy.Field()
    duration = scrapy.Field()
    vehicle = scrapy.Field()
    time_depart = scrapy.Field()

    highlights = scrapy.Field()
    tour_des = scrapy.Field()
    service_des = scrapy.Field()
    view = scrapy.Field()
    url = scrapy.Field()
    related_urls = scrapy.Field()
    image_url = scrapy.Field()