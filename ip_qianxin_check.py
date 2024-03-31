import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()
channels = []
headers={'User-Agent': 'okhttp/3.12.10(Linux;Android9;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36'}
se=requests.Session()
# 初始化计数器为0
counter = 0
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter
    
with open("ip_qianxin.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                channels.append((channel_name, channel_url))
    file.close()
    
def get_redirected_urls(url_list):
    session = requests.Session()
    redirected_urls = []
    for line in url_list:
        increment_counter()
        try:
            channel_name, channel_url = line
            print("==========>>>>>",channel_name, channel_url)
            if '#' not in channel_url:
                try:
                    response = requests.head(channel_url, allow_redirects=False, timeout=2)
                    # 如果初始请求返回200，但之后服务器又发出了302重定向，我们需要处理这种情况
                    if response.status_code == 200 and 'Location' in response.headers:
                        print("1:----------------------------------------------------")
                        print(response.text)
                        # redirected_url = response.headers['Location']
                        # redirected_response = session.head(redirected_url)
                        # new_url = channel_name, redirected_url
                        print("--------------再次定向------》",redirected_url,redirected_response.url)
                        # redirected_urls.append(new_url)
                    # 如果初始请求返回200，但之后服务器又发出了302重定向，我们需要处理这种情况
                    elif response.status_code in [301, 302, 303, 307, 308]:
                        print("--------------直接定向------》",response.headers['Location'])
                        print("2:----------------------------------------------------")
                        print(response.text)
                        # new_url = channel_name, response.headers['Location']
                        # redirected_urls.append(new_url)

                except Timeout:
                    new_url = f"timeout_{channel_name}", channel_url
                    redirected_urls.append(new_url)
                    print("请求超时")
                except requests.RequestException as e:
                    new_url = f"error_{channel_name}", channel_url
                    redirected_urls.append(new_url)
                    print(f"请求发生错误: {e}")
        except:
            print(line)
        
        if counter > 10:
            print(f"执行完成，次数: {counter}")
            break
        
get_redirected_urls(channels)
