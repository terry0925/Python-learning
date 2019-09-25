# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis

class TutorialPipeline(object):

    def __init__(self):
        self.redis_cli = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

    def process_item(self, item, spider):

        self.redis_cli.set(item['id'], str(item))

        return item
