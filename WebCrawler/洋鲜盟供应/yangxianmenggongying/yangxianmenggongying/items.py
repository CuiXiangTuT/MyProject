# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YangxianmenggongyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meat_name = scrapy.Field()
    title = scrapy.Field()
    remarks = scrapy.Field()
    price_0 = scrapy.Field()
    price_1 = scrapy.Field()
    price_2 = scrapy.Field()
    price_3 = scrapy.Field()
    priceGrade_0 = scrapy.Field()
    priceGrade_1 = scrapy.Field()
    priceGrade_2 = scrapy.Field()
    priceGrade_3 = scrapy.Field()
    No = scrapy.Field()
    brand = scrapy.Field()
    factoryNo = scrapy.Field()
    dateOfManufacture = scrapy.Field()
    placeOfOrigin = scrapy.Field()
    qualityGuaranteePeriod = scrapy.Field()
    goodsGrade = scrapy.Field()
    storeName = scrapy.Field()
    store_phone = scrapy.Field()
    location = scrapy.Field()
    cur_time = scrapy.Field()
