# # Define here the models for your scraped items
# #
# # See documentation in:
# # https://docs.scrapy.org/en/latest/topics/items.html
#
# import scrapy
#
#
# class BeefuItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     contact_person_name = scrapy.Field()
#     company = scrapy.Field()
#     phone = scrapy.Field()
#     content = scrapy.Field()
#     cur_time = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeefuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    contact_person_name = scrapy.Field()
    company = scrapy.Field()
    phone = scrapy.Field()
    content = scrapy.Field()
    cur_time = scrapy.Field()
    buy_supply = scrapy.Field()
    location = scrapy.Field()
    product = scrapy.Field()
    new_content = scrapy.Field()
    changhao = scrapy.Field()
    product_name = scrapy.Field()
    pid = scrapy.Field()
