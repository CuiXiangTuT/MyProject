# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RoujiaosuocaigouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meat_name = scrapy.Field()
    sec_catname = scrapy.Field()
    product_name = scrapy.Field()
    buy_requirements = scrapy.Field()
    edittime = scrapy.Field()
    truename = scrapy.Field()
    iphone = scrapy.Field()
    intention_price = scrapy.Field()
    intention_count = scrapy.Field()
    origin_requirements = scrapy.Field()
    province = scrapy.Field()
    city=scrapy.Field()
    status_requirements = scrapy.Field()
    pubbuy = scrapy.Field()
    telcount = scrapy.Field()
    buy_supply = scrapy.Field()
    data_source = scrapy.Field()
    cur_time = scrapy.Field()
    username = scrapy.Field()