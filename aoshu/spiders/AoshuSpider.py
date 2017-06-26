# -*- coding: utf-8 -*-
import scrapy


class AoshuspiderSpider(scrapy.Spider):
    name = "AoshuSpider"
    allowed_domains = ["aoshu.com"]
    start_urls = (
        'http://www.aoshu.com/',
    )

    def parse(self, response):
        pass
