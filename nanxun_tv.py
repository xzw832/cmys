import os
import re
import requests
from requests.exceptions import Timeout

load_urls = [
    "http://tvbox.nx66.bf:99/tvbox/zhibo.php"
    ]
file_contents = []
results = []
for url in load_urls:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        # print(response.text)
        file_contents.append(response.text)
url_list = [line for line_str in file_contents for line in line_str.split('\n')]
def text_list(list_str):
    if len(list_str) > 0:
        if '#genre#' in list_str:
            results.append(list_str)
        elif '#' in list_str:
            part_before_comma = list_str.split(',')[0]
            parts = list(filter(None, list_str.split("#")))
            for line in parts:
                print(line)
                results.append(f"{part_before_comma},{line}")
        else:
            results.append(list)
    
for result in url_list:
    text_list(result)
    # print(result)

# 将结果写入文件
with open("nanxun_tv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        print("======================================")
        print(result)
        file.write(f"{result}\n")
    file.close()
