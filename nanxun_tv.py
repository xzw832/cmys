import os
import re
import requests
from requests.exceptions import Timeout
import chardet

load_urls = [
    "http://tvbox.nx66.bf:99/tvbox/zhibo.php"
    ]
file_contents = []
results = []
for url in load_urls:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        # print(response.text)
        detected_encoding = chardet.detect(response.content)['encoding']
        if detected_encoding is not None:
            content = response.content.decode(detected_encoding, errors='ignore')
        else:
            # 你可以选择一个默认的编码，或者记录一个错误，或者采取其他措施
            content = response.content.decode('utf-8', errors='ignore')
        file_contents.append(content)
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
                count = line.count(',')
                if count == 0:
                    results.append(f"{part_before_comma},{line}")
                else:
                    results.append(f"{line}")
        else:
            results.append(list_str)
    
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
