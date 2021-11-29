# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhongguonongyebushujuchaxunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Carea = scrapy.Field()
    Csource = scrapy.Field()
    CindexName = scrapy.Field()
    Ctime = scrapy.Field()
    product = scrapy.Field()
    itemName = scrapy.Field()
    itemType = scrapy.Field()
    area = scrapy.Field()
    Cperiod = scrapy.Field()
    unit = scrapy.Field()
    Cvalue = scrapy.Field()
    insertTime = scrapy.Field()
