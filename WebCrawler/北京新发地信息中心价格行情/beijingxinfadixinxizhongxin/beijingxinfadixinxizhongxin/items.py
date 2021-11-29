# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeijingxinfadixinxizhongxinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meatSort = scrapy.Field()
    primaryClassification = scrapy.Field()
    secondaryClassification = scrapy.Field()
    prodName = scrapy.Field()
    lowPrice = scrapy.Field()
    avgPrice = scrapy.Field()
    highPrice = scrapy.Field()
    specifications = scrapy.Field()
    place = scrapy.Field()
    unitInfo = scrapy.Field()
    pubDate = scrapy.Field()
    insertTime = scrapy.Field()
    prodID = scrapy.Field()
