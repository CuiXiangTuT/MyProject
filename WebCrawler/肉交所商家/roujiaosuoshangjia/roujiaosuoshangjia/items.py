# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RoujiaosuoshangjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    address = scrapy.Field()
    coordinate = scrapy.Field()
    title = scrapy.Field()
    itemid = scrapy.Field()
    username = scrapy.Field()
    company = scrapy.Field()
    business_addr = scrapy.Field()
    business = scrapy.Field()
    truename = scrapy.Field()
    areaid = scrapy.Field()
    street = scrapy.Field()
    longlat = scrapy.Field()
    cur_time = scrapy.Field()
    shop_num = scrapy.Field()
    phone = scrapy.Field()
