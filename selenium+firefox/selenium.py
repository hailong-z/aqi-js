# -*- coding: utf-8 -*-
#author__hailong__qq_1226619354
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

def parser(data):
    data_1 = data.split(",")
    data_1.pop()
    data_2 = ",".join(data_1)
    return data_2

def save_data(data):
    with open("demo.csv", 'a+', encoding="utf-8") as file:
        file.write(data+"\n")


if __name__ == "__main__":
    option = Options()
    option.headless = True
    browser = webdriver.Firefox(options=option)
    url = 'https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%8A%E6%B5%B7&month=201503'
    browser.get(url)
    time.sleep(3)
    all_day = browser.find_elements_by_xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr')
    for item in all_day:
        item_1 = item.text.replace(" ",",")
        item_2 = item_1.replace("\n", ',')
        res = parser(item_2)
        save_data(res)
    browser.quit()