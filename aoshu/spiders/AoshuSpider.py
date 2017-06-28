# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request


class AoshuspiderSpider(Spider):
    name = "AoshuSpider"
    allowed_domains = ["aoshu.com"]
    start_urls = (
        'http://www.aoshu.com/',
    )
    
    # 用来保持登录状态，可把chrome上拷贝下来的字符串形式cookie转化成字典形式，粘贴到此处
    cookies = { \
        "bdshare_firstime": "1498482879944" ,  \
        "__CITY_URL": "0" ,  \
        "__utmt": "1" ,  
        "__utma": "220146502.546205306.1498482880.1498489116.1498661481.3" ,  
        "__utmb": "220146502.15.10.1498661481" ,  
        "__utmc": "220146502" ,  
        "__utmz": "220146502.1498482880.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic" ,  
        "Hm_lvt_097b4d986b1bd8a9bffe2dd3212a9975": "1498482880,1498661481" ,  
        "Hm_lpvt_097b4d986b1bd8a9bffe2dd3212a9975" : "1498664345"
    }

    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        'Host': 'www.aoshu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理的配置
    meta = {
        #'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def start_requests(self):
        """
        这是一个重载函数，它的作用是发出第一个Request请求
        :return:
        """
        # 带着headers、cookies去请求self.start_urls[0],返回的response会被送到
        # 回调函数parse中
        baseUrl = 'http://www.aoshu.com/tk/asttl/ynj/'
        for i in range(1, 2):
            monthUrl = baseUrl + str(i)
            yield Request(monthUrl, 
                             callback=self.parse, headers=self.headers,
                             cookies=self.cookies, meta=self.meta)    
    def parse(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        
        selector = Selector(response)  # 创建选择器
        print response
        print 'hit pass'        
        pages = response.xpath('//ul[@class="ttl-list"]/li/a/@href').extract()
        
        
        
        print 'parsed'
        print pages
        