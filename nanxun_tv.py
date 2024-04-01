import os
import re
import requests
from requests.exceptions import Timeout

load_urls = [
    "http://mywlkj.ddns.net:754/tv.php?id=63",
    ]
file_contents = []
results = []
for url in load_urls:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        print(response.text)
        file_contents.append(response.text)
url_list = [line for line_str in file_contents for line in line_str.split('\n')]

def text_list(list):
    if len(list) > 0:
        if '#genre#' in list:
            results.append(list)
        elif '#' in list:
            result = line.strip('#')
            for line in result:
                results.append(line)
        else:
            results.append(list)
    
for result in url_list:
    text_list(result)
    print(result)

# 将结果写入文件
with open("nanxun_tv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        print(result)
        file.write(f"{result}\n")
    file.close()
