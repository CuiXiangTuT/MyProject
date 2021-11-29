# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RoupinhuigongyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    buy_supply = scrapy.Field()
    data_source = scrapy.Field()
    productName = scrapy.Field()
    meat_name = scrapy.Field()
    placeOrigin = scrapy.Field()
    factoryNm = scrapy.Field()
    realName = scrapy.Field()
    phone = scrapy.Field()
    releaseTime = scrapy.Field()
    cur_time = scrapy.Field()