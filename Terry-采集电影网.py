import requests
from lxml import etree
import csv
import concurrent.futures
import time

class Caiji:

    def __init__(self):

        self.url = 'https://www.piaohua.com/html/dongzuo/'  # 目标网站
        # 装饰头
        self.head = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    def get_html(self, i):
        response = requests.get(self.url + 'list_' + str(i) + '.html', headers=self.head)  # 拼接url
        print(response.status_code)  # 获取链接信息
        response.encoding = 'utf-8'  # 设置编码utf-8
        return response.text

    def parsel_html(self, data):
        html = etree.HTML(data)  # 将html变成xpath树
        title = html.xpath('//div[@class = "txt"]/h3/a/b/font/text()')  # 电影名称
        profile = html.xpath('//div[@class = "txt"]/p/text()')  # 电影简介
        download_html = html.xpath('//div[@class = "txt"]/span/a/@href')  # 下载地址
        return list(zip(title, profile, download_html))

    def csv_save(self, data):
        # csv 保存
        with open("采集电影网.csv", mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for i in data:
                writer.writerow(i)

    def main(self, i):
        content = self.parsel_html(self.get_html(i))
        return content

if __name__ == '__main__':
    test = Caiji()
    data = []
    page = int(input("请输入要采集的页数："))
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # 利用线程池开辟5个线程
        for i in executor.map(test.main, [k for k in range(1, page)]):  # map函数分配任务
            data.extend(i)
    test.csv_save(data)
    print('多线程运行时间', time.time() - start_time)