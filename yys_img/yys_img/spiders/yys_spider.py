# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from ..items import YysImgItem


class YysSpider(scrapy.Spider):
    name = 'yys_spider'
    
    start_urls = ['http://image.so.com/']
    search_str = '阴阳师'
    search_b = search_str.encode('utf-8')
    
    search_name = '%E9%98%B4%E9%98%B3%E5%B8%88&pd=1&pn=60&correct=%E9%98%B4%E9%98%B3%E5%B8%88'#%加二位十六进制数 url专用的编码
    sn,ps,pc = 130,105,105

    
    #网址1：https://image.so.com/j?q=%E9%98%B4%E9%98%B3%E5%B8%88&pd=1&pn=60&correct=%E9%98%B4%E9%98%B3%E5%B8%88&adstar=0&tab=all&sid=5e5f48670aab2de2b0b4d3b064dbe712&ras=6&cn=0&gn=0&kn=50&crn=0&bxn=20&cuben=0&pornn=0&src=srp&sn=130&ps=105&pc=105
    #网址2：https://image.so.com/j?q=%E9%98%B4%E9%98%B3%E5%B8%88&pd=1&pn=60&correct=%E9%98%B4%E9%98%B3%E5%B8%88&adstar=0&tab=all&sid=5e5f48670aab2de2b0b4d3b064dbe712&ras=6&cn=0&gn=0&kn=50&crn=0&bxn=20&cuben=0&pornn=0&src=srp&sn=190&ps=164&pc=59
           #https://image.so.com/j?q=%E9%98%B4%E9%98%B3%E5%B8%88&pd=1&pn=60&correct=%E9%98%B4%E9%98%B3%E5%B8%88&adstar=0&tab=all&sid=0480f90f220e6eb5500c70fd60747965&ras=6&cn=0&gn=0&kn=50&crn=0&bxn=20&cuben=0&pornn=0&src=srp&sn=190&ps=165&pc=60
    start_urls = ['https://image.so.com/j?q=%s&adstar=0&tab=all&sid=5e5f48670aab2de2b0b4d3b064dbe712&ras=6&cn=0&gn=0&kn=50&crn=0&bxn=20&cuben=0&pornn=0&src=srp&sn=%s&ps=%s&pc=%s' %(search_name, sn, ps, pc)]
    down_maxnum = 1000
    urls = []
    
    
    def parse(self, response):
        res = response.body.decode('utf8') #输出字符

        
        #json.loads(res)['list'][0]['downurl_true']返回第一个图片网址
        infos_list = json.loads(res)['list'] #infos_list
        
        for info in infos_list:
             self.urls.append(info['downurl_true']) #获得一个链接的url列表，接下来呀获取下一个链接的url列表
             
             
        
        down_num = len(self.urls)
        print(len(self.urls))
        img_item = YysImgItem()
        img_item['image_urls'] = self.urls
        yield img_item

        if down_num < self.down_maxnum:
            self.sn = self.sn + 60
            self.ps = self.ps + 60
            next_url = 'https://image.so.com/j?q=%s&adstar=0&tab=all&sid=5e5f48670aab2de2b0b4d3b064dbe712&ras=6&cn=0&gn=0&kn=50&crn=0&bxn=20&cuben=0&pornn=0&src=srp&sn=%s&ps=%s&pc=%s' %(self.search_name, self.sn, self.ps, 60) #需要获取pc的值，目前没在信息中找到，默认60
            yield Request(next_url)
