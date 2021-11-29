# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShihaomuyegongyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    phone = scrapy.Field()
    contact = scrapy.Field()
    standbyPhone = scrapy.Field()
    email = scrapy.Field()
    curTime = scrapy.Field()
