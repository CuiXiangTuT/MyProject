# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShengyibaogongyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meatName = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    price = scrapy.Field()
    contact = scrapy.Field()
    phone = scrapy.Field()
    mobile = scrapy.Field()
    fax = scrapy.Field()
    addr = scrapy.Field()
    postCodes = scrapy.Field()
    cur_time = scrapy.Field()


