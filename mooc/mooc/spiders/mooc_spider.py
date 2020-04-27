# -*- coding: utf-8 -*-

import scrapy
import json
import re
from mooc.items import MoocItem



class MoocSpiderSpider(scrapy.Spider):
    name = 'mooc_spider'
    allowed_domains = ['www.xuexi.cn']
    start_urls = ['https://www.xuexi.cn/lgdata/f547c0f321ac9a0a95154a21485a29d6/1cdd8ef7bfc3919650206590533c3d2a.json?_st=26434284']

    def parse(self, response):
        pydetail = json.loads(response.text)
        DataSets = pydetail['DataSet']
        for DataSet in DataSets:
            dataset = DataSet.rsplit('!')[1]
            dataset_url = 'https://www.xuexi.cn/lgdata/' + dataset + '?_st=26434284'
            yield scrapy.Request(response.urljoin(dataset_url),callback=self.get_list_url)

    def get_list_url(self,response):
        pydetail = json.loads(response.text)
        for i in pydetail:
            list_url = i['url']
            jsurl_list1 = list_url.rsplit('/')[3]
            jsurl_list2 = list_url.rsplit('/')[4].replace('html', 'js')
            new_url = 'https://www.xuexi.cn/' + jsurl_list1 + '/data' + jsurl_list2
            yield scrapy.Request(response.urljoin(new_url),callback=self.get_page_url)

    def get_page_url(self,response):
        jsdetail = response.text.replace('globalCache =', '').replace(';', '')
        pydetail = json.loads(jsdetail)
        get_static_page_url = pydetail['fpe1ki18v228w00']
        for detail in get_static_page_url:
            static_page_url = detail['static_page_url']
            jsurl_list1 = static_page_url.rsplit('/')[3]
            jsurl_list2 = static_page_url.rsplit('/')[4].replace('html', 'js')
            new_url = 'https://www.xuexi.cn/' + jsurl_list1 + '/data' + jsurl_list2
            yield scrapy.Request(response.urljoin(new_url),callback=self.parse_page)
    def parse_page(self,response):
        jsdetail = response.text.replace('globalCache =', '').replace(';', '')
        pydetail = json.loads(jsdetail)
        get_info = pydetail['fp6ioapwuyb80001']['info']
        mooc = get_info['mooc'].strip().replace('\x0b','')
        mooc = re.sub(r'[?*"<>\:|\t\/\\]', '', mooc)
        mooc_class = get_info['mooc_class'].strip().replace('\x0b','')
        mooc_class = re.sub(r'[?*"<>\:|\t\/\\]', '', mooc_class)
        frst_name = get_info['frst_name'].strip().replace('\x0b','')
        frst_name = re.sub(r'[?*"<>\:|\t\/\\]', '', frst_name)[0:101].strip()
        ossUrls = eval(get_info['ossUrl'])
        for i, ossUrl in enumerate(ossUrls):
            file_name = '第' + str(i + 1) + '节' + '.mp4'
            video_url = ossUrl
            item = MoocItem(mooc=mooc,mooc_class=mooc_class,frst_name=frst_name,file_name=file_name,video_url=video_url)
        yield item





