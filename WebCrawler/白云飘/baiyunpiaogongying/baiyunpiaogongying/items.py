# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiyunpiaogongyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meat_kind = scrapy.Field()
    prolist_name = scrapy.Field()
    price = scrapy.Field()
    contact = scrapy.Field()
    phone = scrapy.Field()
    phone1 = scrapy.Field()
    phone2 = scrapy.Field()
    cur_time = scrapy.Field()

