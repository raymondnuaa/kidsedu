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
    
    # �������ֵ�¼״̬���ɰ�chrome�Ͽ����������ַ�����ʽcookieת�����ֵ���ʽ��ճ�����˴�
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

    # ���͸���������httpͷ��Ϣ���е���վ��Ҫαװ�������ͷ������ȡ���е�����Ҫ
    headers = {
        'Host': 'www.aoshu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # ������ķ��ؽ��д��������
    meta = {
        #'dont_redirect': True,  # ��ֹ��ҳ�ض���
        'handle_httpstatus_list': [301, 302]  # ����Щ�쳣���ؽ��д���
    }

    def start_requests(self):
        """
        ����һ�����غ��������������Ƿ�����һ��Request����
        :return:
        """
        # ����headers��cookiesȥ����self.start_urls[0],���ص�response�ᱻ�͵�
        # �ص�����parse��
        baseUrl = 'http://www.aoshu.com/tk/asttl/ynj/'
        for i in range(1, 2):
            monthUrl = baseUrl + str(i)
            yield Request(monthUrl, 
                             callback=self.parse, headers=self.headers,
                             cookies=self.cookies, meta=self.meta)    
    def parse(self, response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        
        selector = Selector(response)  # ����ѡ����
        print response
        print 'hit pass'        
        pages = response.xpath('//ul[@class="ttl-list"]/li/a/@href').extract()
        
        
        
        print 'parsed'
        print pages
        