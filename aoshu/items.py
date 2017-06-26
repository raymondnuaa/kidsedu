# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AoshuItem(scrapy.Item):
    # define the fields for your item here like:
    proTitle  = scrapy.Field()
    proBody   = scrapy.Field()
    proAnswer = scrapy.Field()
    pass
