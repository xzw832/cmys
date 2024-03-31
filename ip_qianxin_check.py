import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
from requests.exceptions import Timeout, RequestException

eventlet.monkey_patch()

channels = []
headers = {'User-Agent': 'okhttp/3.12.10(Linux;Android9;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36'}

def get_redirected_urls(url):
    try:
        session = requests.Session()
        response = session.head(url, allow_redirects=False, timeout=2)
        
        if response.status_code == 200 and 'Location' in response.headers:
            redirected_url = response.headers['Location']
            print("1:----------------------------------------------------")
            print(f"Initial URL: {url}, Redirected URL: {redirected_url}")
        elif response.status_code in [301, 302, 303, 307, 308]:
            redirected_url = response.headers['Location']
            print("2:----------------------------------------------------")
            print(f"Redirected URL: {redirected_url}")
        else:
            print(f"Response Status Code: {response.status_code}")
    except RequestException as e:
        print(f"Error occurred for URL {url}: {e}")

with open("ip_qianxin.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                channels.append((channel_name, channel_url))

for channel_name, channel_url in channels:
    try:
        get_redirected_urls(channel_url)
        time.sleep(1)
    except RequestException as e:
        print(f"Error occurred for URL {url}: {e}")
        continue
