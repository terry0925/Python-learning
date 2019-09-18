# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class WeibocommentsspiderPipeline(object):

    def __init__(self):
        self.file = open('weibo.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        data = json.dumps(item, ensure_ascii=False)
        self.file.write(data + '\n')
        return item

    def close_spider(self, spider):
        self.file.close()
