import random
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queue import Queue
import threading
from concurrent.futures import ThreadPoolExecutor

import time
import os
import re
from bs4 import BeautifulSoup
import requests

lock = threading.Lock()
now_today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
# 线程安全的队列，用于存储下载任务
task_queue = Queue()

def cut_first_chinese_words(text, num=2):
    for i, char in enumerate(text):
        if char >= '\u4e00' and char <= '\u9fa5':
            return text[:i+2]
    return 'xxxxxxxxxxxxxxxxxx'
    
#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

urls = [
    "东海新闻,http://114.233.127.18:8888/rtp/239.49.9.48:6000",
    "南京娱乐,http://180.113.159.91:8800/rtp/239.49.8.229:6000"
    ]


def modify_urls(http_url):
    modified_urls = []
    channel,url = http_url.split(',')
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find("/", ip_start_index)  # 查找下一个"/"的位置，用来确定IP地址的结束位置
    
    # 提取IP地址
    if ip_end_index != -1:
        ip_address = url[ip_start_index:ip_end_index]
    else:
        # 如果没有找到下一个"/"，则假设URL的末尾就是IP地址的结束位置
        ip_address = url[ip_start_index:]
    # 分割IP地址和端口
    new_ip_address, port = ip_address.split(':')
    # 分割IP地址的各个部分
    new_ip_address = new_ip_address.split('.')
    # 把尾位（最后一个部分）变成1
    new_ip_address[-1] = '1'
    # 重新组合IP地址的各个部分
    ip_address = '.'.join(new_ip_address)
    ip_start = url[:ip_start_index]
    ip_end = url[ip_end_index:]
    for i in range(1, 255):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{channel},{ip_start}{modified_ip}:{port}{ip_end}"
        print(modified_url)
        modified_urls.append(modified_url)
    return modified_urls

def is_url_accessible(url):
    try:
        return url
    except requests.exceptions.RequestException:
        pass
    # return None
    return url
# 初始化计数器为0
counter = -1
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

valid_urls = []
#   多线程获取可用url
for ipv in urls:
    url = ipv.strip()
    modified_urls = modify_urls(url)
    valid_urls.append(modified_urls)
    
            
sorted_list = list(set(valid_urls))    # 去重得到唯一的URL列表
resultslist = sorted(sorted_list)

with open("seekip.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.write(f"{now_today}更新IP组\n")
    file.close()
