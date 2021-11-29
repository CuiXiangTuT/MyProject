# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NiurouhuigongyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meatSort = scrapy.Field()
    title = scrapy.Field()
    orderQuantity = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    marketPrice = scrapy.Field()
    marketPriceUnit = scrapy.Field()
    placeOfShipment = scrapy.Field()
    contact = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    curTime = scrapy.Field()
