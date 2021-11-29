# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YimutianchandihangqingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meatClass = scrapy.Field()
    address = scrapy.Field()
    meatSort = scrapy.Field()
    price = scrapy.Field()
    changeTrend = scrapy.Field()
    Ctime = scrapy.Field()
    detailMeat = scrapy.Field()
    detailPrice = scrapy.Field()
    detailChangeTrend = scrapy.Field()
    insertTime = scrapy.Field()
