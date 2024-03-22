import random
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
from bs4 import BeautifulSoup
from queue import Queue
import threading

lock = threading.Lock()
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
urls = [
    "http://tonkiang.us/hoteliptv.php?page=1&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=2&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=1&s=揭阳",
    "http://tonkiang.us/hoteliptv.php?page=2&s=揭阳",
    "http://tonkiang.us/hoteliptv.php?page=1&s=珠海",
    "http://tonkiang.us/hoteliptv.php?page=1&s=广州",
    "http://tonkiang.us/hoteliptv.php?page=2&s=广州",
    "http://tonkiang.us/hoteliptv.php?page=1&s=汕头",
    "http://tonkiang.us/hoteliptv.php?page=2&s=汕头",
    "http://tonkiang.us/hoteliptv.php?page=1&s=深圳",
    "http://tonkiang.us/hoteliptv.php?page=2&s=深圳",
    "http://tonkiang.us/hoteliptv.php?page=1&s=广东",
    "http://tonkiang.us/hoteliptv.php?page=2&s=广东",
    "http://tonkiang.us/hoteliptv.php?page=1&s=新闻",
    "http://tonkiang.us/hoteliptv.php?page=2&s=新闻",
    "http://tonkiang.us/hoteliptv.php?page=1&s=综合",
    "http://tonkiang.us/hoteliptv.php?page=2&s=综合",
    "http://tonkiang.us/hoteliptv.php?page=1&s=北京",
    "http://tonkiang.us/hoteliptv.php?page=1&s=上海",
    "http://tonkiang.us/hoteliptv.php?page=1&s=香港",
    "http://tonkiang.us/hoteliptv.php?page=2&s=香港",
    "http://tonkiang.us/hoteliptv.php?page=1&s=重庆",
    "http://tonkiang.us/hoteliptv.php?page=1&s=苏州",
    "http://tonkiang.us/hoteliptv.php?page=1&s=成都",
    "http://tonkiang.us/hoteliptv.php?page=1&s=杭州",
    "http://tonkiang.us/hoteliptv.php?page=1&s=厦门",
    "http://tonkiang.us/hoteliptv.php?page=2&s=厦门",
    "http://tonkiang.us/hoteliptv.php?page=1&s=美国"
    ]
# 初始化计数器为0
counter = -1
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)  # 10秒后超时
    # 设置脚本执行超时
    driver.set_script_timeout(50)  # 5秒后超时
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(20)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()
    print(increment_counter())    #方便看看是否有执行啊
    # 查找所有符合指定格式的网址
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls_y = set(urls_all)  # 去重得到唯一的URL列表
    for urlv in urls_y:
        resultslist.append(f"{urlv}")

resultslist = set(resultslist)    # 去重得到唯一的URL列表

with open("iplist.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.close()
