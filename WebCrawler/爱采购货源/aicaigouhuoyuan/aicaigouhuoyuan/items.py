# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AicaigouhuoyuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id_acg = scrapy.Field()
    category = scrapy.Field()
    qid = scrapy.Field()
    from_source = scrapy.Field()
    location = scrapy.Field()
    query = scrapy.Field()
    fullname = scrapy.Field()
    category_ = scrapy.Field()
    priceCurrency = scrapy.Field()
    price = scrapy.Field()
    unitCode = scrapy.Field()
    minValue = scrapy.Field()
    maxValue = scrapy.Field()
    contact = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    contactName = scrapy.Field()
    wechatNumber = scrapy.Field()
    externalAddress = scrapy.Field()
    address_v2 = scrapy.Field()
    address = scrapy.Field()
    addr = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    userDetail = scrapy.Field()
    provider_name = scrapy.Field()
    provider_status = scrapy.Field()
    provider_regCap = scrapy.Field()
    provider_regAddr = scrapy.Field()
    provider_scope = scrapy.Field()
    provider_jumpUrl = scrapy.Field()
    cur_time = scrapy.Field()
    query_ = scrapy.Field()
