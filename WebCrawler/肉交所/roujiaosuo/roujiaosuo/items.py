# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RoujiaosuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    meat_name = scrapy.Field()
    sec_catname = scrapy.Field()
    product_name = scrapy.Field()
    thumb = scrapy.Field()
    company = scrapy.Field()
    good_sort = scrapy.Field()
    good_chandi = scrapy.Field()
    good_changhao = scrapy.Field()
    good_price = scrapy.Field()
    good_count = scrapy.Field()
    good_cangku = scrapy.Field()
    contact_person_name = scrapy.Field()
    contact_person_img = scrapy.Field()
    contact_person_phone = scrapy.Field()
    merchant_url = scrapy.Field()
    update_time = scrapy.Field()
    buy_supply = scrapy.Field()
    data_source = scrapy.Field()
    cur_time = scrapy.Field()
    username = scrapy.Field()
    business = scrapy.Field()
