# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiwuqigongyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meatName = scrapy.Field()
    title = scrapy.Field()
    phone = scrapy.Field()
    contact = scrapy.Field()
    company = scrapy.Field()
    publishTime = scrapy.Field()
    cur_time = scrapy.Field()

