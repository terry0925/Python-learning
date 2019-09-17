# -*- coding: utf-8 -*-
import scrapy
import redis
import json
class QuotesSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'referer': 'https://www.zhihu.com/people/ponyma/followers?page=6'
        }
    start_urls = ['https://www.zhihu.com/api/v4/members/ponyma/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=10']
    #response = scrapy.Request(start_urls, headers=header)

    def parse(self, response):
        jsonj = json.loads(response.text)
        for user in jsonj['data']:
            yield user
            #  print(str(user))
            #  self.upload_to_database(user)

        next_page = jsonj['paging']['next']
        # print(next_page)
        if next_page:
            next_page = next_page.replace('https://www.zhihu.com/members/ponyma/followers', 'https://www.zhihu.com/api/v4/members/ponyma/followers')
            yield scrapy.Request(next_page, callback=self.parse)


    # def make_connect(self):
    #     r = redis.Redis(host='127.0.0.1', port=6379, db=1)
    #     return r
    #
    # def upload_to_database(self, data):
    #     session = self.make_connect()
    #     session.set(data['id'], str(data))

