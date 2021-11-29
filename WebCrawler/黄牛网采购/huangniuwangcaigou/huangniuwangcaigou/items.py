# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HuangniuwangcaigouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goodsId = scrapy.Field()
    goodsName = scrapy.Field()
    minUnitPrice = scrapy.Field()
    maxUnitPrice = scrapy.Field()
    totalCount = scrapy.Field()
    goodsUnit = scrapy.Field()
    endingDate = scrapy.Field()
    title = scrapy.Field()
    placeAll = scrapy.Field()
