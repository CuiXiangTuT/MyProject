# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DongpinyigangshanghudatingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    update_time = scrapy.Field()
    packageUnit = scrapy.Field()
    origin = scrapy.Field()
    companyName = scrapy.Field()
    goodsCategory = scrapy.Field()
    goodsAmount = scrapy.Field()
    isOpenPayment = scrapy.Field()
    factoryNo = scrapy.Field()
    cityId = scrapy.Field()
    title = scrapy.Field()
    memberGradeId = scrapy.Field()
    cityName = scrapy.Field()
    unitId = scrapy.Field()
    u_id = scrapy.Field()
    unitName = scrapy.Field()
    provinceId = scrapy.Field()
    userId = scrapy.Field()
    specificationValue = scrapy.Field()
    companyId = scrapy.Field()
    productCode = scrapy.Field()
    isTop = scrapy.Field()
    goodsPrice = scrapy.Field()
    provinceName = scrapy.Field()
    address = scrapy.Field()
    licenseImage = scrapy.Field()
    business_name = scrapy.Field()
    StartingBatch = scrapy.Field()
    isBill = scrapy.Field()
    cur_time = scrapy.Field()
    contactsPhone = scrapy.Field()
    goodsType =scrapy.Field()
    goodsTypeDetail = scrapy.Field()