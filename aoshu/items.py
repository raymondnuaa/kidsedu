# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class AoshuItem(scrapy.Item):
    # define the fields for your item here like:
    item_type = scrapy.Field()
    title    = scrapy.Field()
    question = scrapy.Field()
    answer   = scrapy.Field()
    datime   = scrapy.Field()
    
    image_urls  = scrapy.Field()
    images      = scrapy.Field()
    image_paths = scrapy.Field()
    
class AoshuItemLoader(ItemLoader):
    default_item_class = AoshuItem
    #default_output_processor = TakeFirst()  
