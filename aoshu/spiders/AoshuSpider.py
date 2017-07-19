# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy.utils.python import to_native_str
from six.moves.urllib.parse import urljoin

from aoshu.items import AoshuItemLoader

'''
>scrapy shell http://www.aoshu.com/tk/asttl/ynj/1
Then get the 301 response status

>rdUrl = response.headers['Location']
>fetch(rdUrl)

Then the response is updated with the 200


Adding below two lines in your code to inspect the response in spider
#from scrapy.shell import inspect_response
#inspect_response(response, self)
'''

class AoshuspiderSpider(Spider):
    name = "AoshuSpider"
    allowed_domains = ["aoshu.com"]
    #start_urls = (
    #    'http://www.aoshu.com/',
    #)
    
    # �������ֵ�¼״̬���ɰ�chrome�Ͽ����������ַ�����ʽcookieת�����ֵ���ʽ��ճ�����˴�
    cookies = {}

    # ���͸���������httpͷ��Ϣ���е���վ��Ҫαװ�������ͷ������ȡ���е�����Ҫ
    headers = {
        'Host': 'www.aoshu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # ������ķ��ؽ��д��������
    meta = {
        'dont_redirect': True,  # ��ֹ��ҳ�ض���
        'handle_httpstatus_list': [301, 302]  # ����Щ�쳣���ؽ��д���
    }

    def start_requests(self):
        """
        ����һ�����غ��������������Ƿ�����һ��Request����
        :return:
        """
        # ����headers��cookiesȥ����self.start_urls[0],���ص�response�ᱻ�͵�
        # �ص�����parse��
        #baseUrl = 'http://www.aoshu.com/tk/asttl/ynj/'
        #baseUrl = 'http://www.aoshu.com/tk/asttl/enj/'
        #baseUrl = 'http://www.aoshu.com/tk/asttl/snj/'
        #baseUrl = 'http://www.aoshu.com/tk/asttl/sinj/'
        #baseUrl = 'http://www.aoshu.com/tk/asttl/wnj/'
        baseUrl = 'http://www.aoshu.com/tk/asttl/lnj/'
        for i in range(1, 13):
            monthUrl = baseUrl + str(i)
            yield Request(monthUrl, 
                             callback=self.parse, headers=self.headers,
                             cookies=self.cookies, meta=self.meta)    
    def parse(self, response):
        if response.status >= 300 and response.status < 400:

            # HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
            location = to_native_str(response.headers['location'].decode('latin1'))

            # get the original request
            request = response.request
            # and the URL we got redirected to
            redirected_url = urljoin(request.url, location)

            if response.status in (301, 307) or request.method == 'HEAD':
                redirected = request.replace(url=redirected_url)
                yield redirected
            else:
                redirected = request.replace(url=redirected_url, method='GET', body='')
                redirected.headers.pop('Content-Type', None)
                redirected.headers.pop('Content-Length', None)
                yield redirected
        
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        
        #selector = Selector(response)  # ����ѡ����

        pages = response.xpath('//ul[@class="ttl-list"]/li/a/@href').extract()
        for page in pages:
            if(len(page) > 5):
                yield Request(page, callback=self.question_parse, headers=self.headers,
                                cookies=self.cookies, meta=self.meta)
        
    def question_parse(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        
        selector = Selector(response)        
        
        l = AoshuItemLoader(response=response, selector=selector)
        l.add_value('item_type',  'question')
        l.add_xpath('title',      '//h1[@class="tit-art tc"]/text()')
        l.add_xpath('question',   '//div[@class="content"]/p/text()')       
        l.add_xpath('image_urls', '//div[@class="content"]/p[2]/strong/img/@src')
        l.add_xpath('image_urls', '//div[@class="content"]/p[2]/img/@src')
        
        yield l.load_item()     

        answerPages = response.xpath('//div[@class="btn-pages"]/a[2]/@href').extract()
        for page in answerPages:
            if(len(page) > 5):
                yield Request(page, callback=self.answer_pasrse, headers=self.headers,
                                cookies=self.cookies, meta=self.meta)
        
    def answer_pasrse(self, response): 
        selector = Selector(response)        
        
        l = AoshuItemLoader(response=response, selector=selector)
        l.add_value('item_type',  'answer')
        l.add_xpath('title',      '//h1[@class="tit-art tc"]/text()')
        l.add_xpath('answer',     '//div[@class="content"]/p/text()')   
        l.add_xpath('answer',     '//div[@class="content"]/p[2]/text()')   
        l.add_xpath('image_urls', '//div[@class="content"]/p[2]/strong/img/@src')
        l.add_xpath('image_urls', '//div[@class="content"]/p[2]/img/@src')
        
        yield l.load_item() 


        
        