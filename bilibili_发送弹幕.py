import requests
import time

url = 'https://api.live.bilibili.com/msg/send'

header = {
 'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0"
}

datas = {
    'color': '16777215',
    'fontsize': '25',
    'mode': '1',
    'msg': 'abcabc',
    'rnd': '1567442415',
    'roomid': '21441066',
    'bubble': '0',
    'csrf_token': '23aab0ebe53af689554a6468d820906e',
    'csrf': '23aab0ebe53af689554a6468d820906e'}

cookie = {"Cookie":"_uuid=50829E94-2BB4-485A-EB7C-5454A9F83C9491201infoc; buvid3=73067CAF-A1E6-441D-A52E-532D56A5160B155825infoc; LIVE_BUVID=AUTO8615670668924577; sid=4jlqg4r6; DedeUserID=471100445; DedeUserID__ckMd5=3723b06e5a0e05b2; SESSDATA=eac56cab%2C1569658916%2C29b9d281; bili_jct=23aab0ebe53af689554a6468d820906e; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1567066926,1567442402; UM_distinctid=16cdc92459a9-02455af66148f38-4a5568-13c680-16cdc92459c1d; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1567442420; _dfcaptcha=afbc829d9d6d1b8e1319b42cdd263618"}
print(cookie)
for i in range(10):
    time.sleep(1)
    datas['msg'] = str(i)
    print(datas)
    response = requests.post(url, headers=header, data=datas, cookies=cookie)
    print(response.status_code)


