import config
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

# 查找所有符合指定格式的网址
infoList = []
urls_y = []
urls = [
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%87%A4%E5%87%B0",
    "http://tonkiang.us/hoteliptv.php?page=2&s=%E5%87%A4%E5%87%B0",
    "http://tonkiang.us/hoteliptv.php?page=3&s=%E5%87%A4%E5%87%B0",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E6%B1%95%E5%A4%B4",
    "http://tonkiang.us/hoteliptv.php?page=2&s=%E6%B1%95%E5%A4%B4",
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E7%94%B5%E5%BD%B1"
    ]

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=chrome_options)
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(10)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()

    # 查找所有符合指定格式的网址
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls_y = urls_y + set(urls_all)  # 去重得到唯一的URL列表
    
with open("iplist.txt", 'w', encoding='utf-8') as file:
    for urlv in urls_y:
        file.write(urlv + "\n")
        print(urlv)
    file.close()
