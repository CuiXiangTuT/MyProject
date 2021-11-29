# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DongpinyigangcaigouyixiangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    goodsCategory = scrapy.Field()
    origin = scrapy.Field()
    provinceId = scrapy.Field()
    provinceName = scrapy.Field()
    cityId = scrapy.Field()
    cityName = scrapy.Field()
    contactsPhone = scrapy.Field()
    goodsAmount = scrapy.Field()
    priceType = scrapy.Field()
    priceTypeDetail = scrapy.Field()
    goodsPrice = scrapy.Field()
    details = scrapy.Field()
    update_Date = scrapy.Field()
    companyId = scrapy.Field()
    userId = scrapy.Field()
    goodsType = scrapy.Field()
    goodsTypeRequirement = scrapy.Field()
    cur_time = scrapy.Field()
    companyName = scrapy.Field()
    address = scrapy.Field()
