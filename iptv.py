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
    "https://raw.githubusercontent.com/taijichadao/tv/main/itvlist.txt",
    "http://api.mcqq.cn/tvbox/zhibo.php",
    "http://tvbox.nx66.bf:99/tvbox/zhibo.php",
    "http://mywlkj.ddns.net:754/tv.php",
    "https://raw.gitcode.com/lionzang/TV/raw/main/channel.txt"
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
file_contents = []
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
    print(page_content)    #方便看看是否有执行啊
    file_contents.append(page_content)
    
with open("iptv_all.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    output.close()
