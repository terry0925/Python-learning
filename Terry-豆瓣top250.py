import re
import requests
import concurrent.futures
import csv
from openpyxl import Workbook
import json
import threading
import time
'''
目标站点：https://movie.douban.com/top250


1. 请求网址获取数据(requests.get)
2. 使用正则表达式提取数据(re.findall)
3. 利用线程池分配多个线程执行任务
3. 最后将数据分别保存为csv，json，xlsx.

**Author**: Terry
'''

#利用compile方法构建规则
r = re.compile('<li>.*?<span class="title">(.*?)</span>.*?<p class="">(.*?)&nbsp;(.*?)<br>(.*?)&nbsp;/&nbsp;.*?<span class="rating_num" property="v:average">(.*?)</span>.*?</li>', re.S)

class DouBan_(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = 'https://movie.douban.com/top250?start='
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    def get_html(self, i):
        #拼接网页字符串
        response = requests.get(url=self.base_url+str(i), headers=self.header)
        #解析网页内容并返回结果
        response.encoding = 'utf-8'
        html = response.text
        return html

    def parsel_html(self, html):
        #定义空list用于存放解析一个网页内容的返回结果
        list_ = []
        #正则表达是解析内容
        dds = re.findall(r, html)
        #格式化解析结果去除空格
        for i in dds:
            list_dds = list(i)
            list_dds[1] = list_dds[1].strip()
            list_dds[2] = list_dds[2].replace("&nbsp;", '')
            if list_dds[2][0:2] != '主演':  # 修改异常数据（无主演）
                list_dds[2] = None
            list_dds[3] = list_dds[3].strip()
            list_.append(list_dds)
        return list_

    def save_data(self, data):
        self.csv_save(data)
        self.json_save(data)
        self.excel_save(data)

    def csv_save(self, data):
        # csv 保存
        with open("data_csv.csv", mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for i in data:
                writer.writerow(i)

    def json_save(self, data):
        # json 保存
        dict_ = {}
        for i in data:
            dict_[i[0]] = i[1:-1]
        json_str = json.dumps(dict_, ensure_ascii=False)
        with open("json_file.json", mode='w', encoding='utf-8') as f:
            f.write(json_str)

    def excel_save(self, data):
        # xlsx 保存
        wb = Workbook()
        sheet = wb.active
        for i in data:
            sheet.append(i)
        wb.save('excel_save.xlsx')


    def start(self, page=0, *args, **kwargs):
        print("正在爬取{0}".format(page))
        html_data = self.get_html(page)
        return self.parsel_html(html_data)

if __name__ == '__main__':
    start_time = time.time()
    test = DouBan_()
    data = []
    # 测试时间
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # 利用线程池开辟5个线程
        for i in executor.map(test.start, [k for k in range(0, 250, 25)]):  # map函数分配任务
            data.extend(i)
    test.save_data(data)
    print('多线程运行时间', time.time() - start_time)