# -*- coding: utf-8 -*-
import scrapy
import json
import re
'''
知乎爬全站的信息包括followers & followees

Author Terry
'''


class QuotesSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'referer': 'https://www.zhihu.com/people/ponyma/followers?page=6'
        }
    start_urls = ['https://www.zhihu.com/api/v4/members/ponyma/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20']


    def parse(self, response):
        jsonj = json.loads(response.text)
        #  提取当前response URL，并且拼接尾部字符串使得下面提取的followers和followees
        #  都是从他们的各自的首页开始爬取
        url = re.search('https://(.*?)&offset', response.url).group(1) + '&offset=0&limit=10'
        #  定义followers的url
        followers_list = []
        #  定义followees的url
        followees_list = []

        if len(jsonj['data']):  # 判断是否有followers
            for user in jsonj['data']:
                usr_token = user['url_token']  # 获取followers or followees 用户名
                token_combine = f'members/{usr_token}/'  # 拼接 followers or followees 的url字符串
                follow_url = re.sub('members/(.*?)/', token_combine, url)  # 创建 followers or followees 的请求url
                if 'followers' in response.url:  # 判断如果当前请求是followers，则把当前 request URL 加入followers_list
                    followers_list.append(f'https://{follow_url}')
                    followees_list.append(f'https://{follow_url}'.replace('followers', 'followees'))  #
                else: #  如果不是则为 followees，把当前 request URL 加入followees_list
                    followees_list.append(f'https://{follow_url}')
                    followers_list.append(f'https://{follow_url}'.replace('followees', 'followers'))

                yield user

        for followers in followers_list:
            yield scrapy.Request(followers, callback=self.parse)

        for followees in followees_list:
            yield scrapy.Request(followees, callback=self.parse)


        print('*' * 80)
        print(f'已经完成当前页 ：{response.url}')
        # print(next_page)
        if not jsonj['paging']['is_end']:
            next_page = jsonj['paging']['next']
            next_page = next_page.replace('https://www.zhihu.com', 'https://www.zhihu.com/api/v4')
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            print('*' * 80)
            print(f'准备爬取下一页：{next_page}')









