# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re

class MyImagesPipeline(ImagesPipeline):
    #def get_media_requests(self, item, info):
    #    for image_url in item['image_urls']:
    #        yield scrapy.Request(image_url)

    #def file_path(self, request, response=None, info=None):
    #    #item=request.meta['item'] # Like this you can use all from item, not just url.
    #    imagePath = request.url.split('/')
    #    return 'full/%s-%s-%s' % (imagePath[-4], imagePath[-3], imagePath[-2])
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            item['image_paths'] = ''
            #raise DropItem("Item contains no images")
        else:
            item['image_paths'] = image_paths
        return item
    
    #def item_completed(self, results, item, info):
    #    datime = re.search('(\d+.\d+)', item['title'][0])
    #    print '-------=====%s=====-----' % datime
    #    item['image_paths'] = 'full/%s.jpg' % datime.group(1)

class AoshuPipeline(object):
    def process_item(self, item, spider):
        print "---------------------------------------------------------------"        
        fileQuestion = open("itemQues.txt", "a")  # 以追加的方式打开文件，不存在则创建
        fileAnwser   = open("itemAnws.txt", "a") 
        # 因为item中的数据是unicode编码，为了在控制台中查看数据的有效性和保存，
        # 将其编码改为utf-8
        
        #itemStr      = str(item).decode("unicode_escape").encode('utf-8')
        #itemTitle    = item['title'][0].decode("gb2312").encode('utf-8')
        #itemQuestion = item['question'][0].decode("gb2312").encode('utf-8')
        
        itemType    = item['item_type'][0].encode('utf-8').strip()
        itemTitle   = item['title'][0].encode('utf-8').strip()
        if(item['image_paths'] != ''):
            itemImgPath = item['image_paths'][0].encode('utf-8').strip()
        else:
            itemImgPath = ''
        if(itemType == 'question'):
            itemQuestion = ''
            for itemQues in item['question']:
                #说明
                if(itemQues == u'\r\n\t\u3000\u3000\u8bf4\u660e\uff1a'):
                    break
                #奥数天天练栏
                elif(itemQues.startswith(u'\r\n\t\u3000\u3000\xb7\u5965\u6570\u5929\u5929\u7ec3\u680f')):
                    break
                else:
                    itemTmp = itemQues.encode('utf-8').strip().replace('\r\n', '').strip()
                    itemQuestion += itemTmp
                
            fileQuestion.write(itemTitle)
            fileQuestion.write('\n')
            fileQuestion.write(itemQuestion)
            fileQuestion.write('\n')
            fileQuestion.write(itemImgPath)
            fileQuestion.write('\n;\n\n')
            fileQuestion.close()
        elif (itemType == 'answer'):
            itemAnws = ''
            for itemAnwser in item['answer']:
                itemAnws += itemAnwser.encode('utf-8').strip()
            fileAnwser.write(itemTitle)
            fileAnwser.write('\n')
            fileAnwser.write(itemAnws)
            fileAnwser.write('\n')
            fileAnwser.write(itemImgPath)
            fileAnwser.write('\n;\n\n')
            fileAnwser.close()   
        #print itemStr  #在控制台输出
        return item  # 会在控制台输出原item数据，可以选择不写
        
        #UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-12: ordinal not in range(128)
