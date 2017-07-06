# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DrawlehouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()     # 面积
    avgPrice = scrapy.Field()
    address = scrapy.Field()

class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

