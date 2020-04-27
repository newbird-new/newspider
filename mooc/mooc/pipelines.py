# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request
class MoocPipeline(object):
    def open_spider(self, spider):
        print("爬虫开始了......" * 5)


    def process_item(self, item, spider):
        mooc = item['mooc']
        mooc_class = item['mooc_class']
        frst_name = item['frst_name']
        file_name = item['file_name']
        video_url = item['video_url']
        # muke_path = os.path.join(os.path.dirname(__file__), '慕课视频')
        muke_path = 'D:\慕课视频'
        if not os.path.exists(muke_path):
            os.makedirs(muke_path)
        mooc_class_path = os.path.join(muke_path, mooc, mooc_class, frst_name)
        if not os.path.exists(mooc_class_path):
            os.makedirs(mooc_class_path)
        file_name_path = os.path.join(mooc_class_path, file_name)
        if not os.path.exists(file_name_path):
            try:
                request.urlretrieve(video_url, file_name_path)
                print('下载 ' + mooc + mooc_class + frst_name + file_name + '完成')
            except:
                count = 1
                while count <= 5:
                    try:
                        request.urlretrieve(video_url, file_name_path)
                        break
                    except:
                        count += 1
                if count > 5:
                    print(mooc + mooc_class + frst_name + file_name + '下载失败')
        else:
            print(mooc + mooc_class + frst_name + file_name + '  已经下载完毕啦！！！')

        return item

    def close_spider(self, spider):
        print("爬虫结束了！！！！" * 5)

