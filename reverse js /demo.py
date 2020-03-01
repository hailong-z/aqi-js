# -*- coding: utf-8 -*-
#author__hailong__qq_1226619354
import json
from pprint import pprint
import requests
import execjs
import re
from js import _js
import jsonpath


class Demo:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'none',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.params = {
            'city': '上海',
            'month': '201503',
    }

    def get_index(self):
        response = self.session.get('https://www.aqistudy.cn/historydata/daydata.php', headers=self.headers, params=self.params, verify=False)
        encrypt_url = re.search('(resource/js/encrypt_.*?)"', response.text).group(1)
        return 'https://www.aqistudy.cn/historydata/' + encrypt_url

    def get_data(self, url):
        response = self.session.get(url, headers=self.headers, verify=False)
        js = execjs.compile('function return_p(){return '+response.text[5: -2]+'}')
        js_text = js.call('return_p')
        re_text = re.findall('(.*?;function (\w+)\(method,object,callback,period.*?)\$\.ajax.*?data:{(.*?):', js_text)
        main_code = _js + re_text[0][0]+'return param}}'
        return_param = re_text[0][1]
        param = re_text[0][2]
        callback = re.search('}function (\w+)\(data\){data=BASE64\.decrypt\(data\);data=DES\.decrypt\(', js_text).group(1)
        js_code = execjs.compile(main_code)
        data = {param: js_code.call(return_param, 'GETDAYDATA', self.params, "", 6)}
        response = self.session.post('https://www.aqistudy.cn/historydata/api/historyapi.php', headers=self.headers, data=data, verify=False)
        response = js_code.call(callback, response.text)
        data_res = json.loads(response)
        return data_res

    def main(self):
        encrypt_url = self.get_index()
        data_jsons = self.get_data(encrypt_url)
        return data_jsons


"""
时间  AQI  范围  质量等级  PM2.5  PM10  SO2  CO NO2
   'aqi': 109,
   'co': 0.9,
   'no2': 39,
   'o3': 112,
   'pm10': 62,
   'pm2_5': 82,
   'quality': '轻度污染',
   'rank': '313',
   'so2': 17,
   'time_point': '2015-03-03'
"""
if __name__ == '__main__':
    res_json = Demo().main() #dict
    items = jsonpath.jsonpath(res_json, '$..items')
    file_h = open("demo.csv",'w',encoding='utf-8')
    file_h.write("时间,AQI,范围,质量等级,PM2.5,PM10,SO2,CO,NO2\n")
    file_h.close()
    # pprint(items[0])
    for item in items[0]:
        # print(item)
        data = f"{item['time_point']}," \
               f"{item['aqi']}," \
               f"{item['rank']}," \
               f"{item['quality']}," \
               f"{item['pm2_5']}," \
               f"{item['pm10']}," \
               f"{item['so2']}," \
               f"{item['co']}," \
               f"{item['no2']}\n"
        with open("demo.csv" , 'a+',encoding="utf-8") as file:
            file.write(data)





