# -*- coding: utf-8 -*-
import scrapy
import json

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://m.weibo.cn/api/container/getIndex?display=0&retcode=6102&type=uid&value=2830678474&containerid=1076032830678474&page=1']


    def parse(self, response):
        json_response = json.loads(response.text, encoding='utf-8')
        #print(response.url)
        for data in json_response['data']['cards']:
                content = data['mblog'].get('raw_text', data['mblog']['text'])
                create_date = data['mblog'].get('created_at', '2019')
                comments_count = data['mblog'].get('comments_count', '0')
                attitudes_count = data['mblog'].get('attitudes_count', '0')
                dict_result = {
                    '内容': content,
                    '日期': create_date,
                    '评论数': comments_count,
                    '点赞数': attitudes_count
                }
                yield dict_result
        next_page = json_response['ok']
        if next_page:
            page = json_response['data']['cardlistInfo']['page']
            next_page = 'https://m.weibo.cn/api/container/getIndex?display=0&retcode=6102&type=uid&value=2830678474&containerid=1076032830678474&page=' + str(page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



