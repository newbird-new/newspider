# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocItem(scrapy.Item):
    # define the fields for your item here like:
    mooc = scrapy.Field()
    mooc_class = scrapy.Field()
    frst_name = scrapy.Field()
    file_name = scrapy.Field()
    video_url = scrapy.Field()

