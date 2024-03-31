import os
import re
import requests
from requests.exceptions import Timeout

load_urls = [
    "http://mywlkj.ddns.net:754/tv.php?id=63",
    ]
file_contents = []
with open("mywlkj_gt.txt", 'r', encoding='utf-8') as file:
    file_contents = file.readlines()
    
def get_redirected_urls(url_list):
    session = requests.Session()
    redirected_urls = []
    for line in url_list:
        try:
            line = line.strip()
            count = line.count(',')
            if count == 1:
                if line:
                    channel_name, channel_url = line.split(',')
                    print("==========>>>>>",channel_name, channel_url)
                    if '#' not in channel_url and 'mp4' not in channel_url:
                        try:
                            response = requests.head(channel_url, allow_redirects=False, timeout=1.5)
                            # 如果初始请求返回200，但之后服务器又发出了302重定向，我们需要处理这种情况
                            if response.status_code == 200 and 'Location' in response.headers:
                                redirected_url = response.headers['Location']
                                redirected_response = session.head(redirected_url)
                                new_url = channel_name, redirected_url
                                print("--------------再次定向------》",redirected_url,redirected_response.url)
                                redirected_urls.append(new_url)
                            # 如果初始请求直接返回了重定向，我们直接返回重定向的URL
                            elif response.status_code in [301, 302, 303, 307, 308]:
                                print("--------------直接定向------》",response.headers['Location'])
                                new_url = channel_name, response.headers['Location']
                                redirected_urls.append(new_url)
                            else:
                                # 如果没有重定向，返回原始URL
                                new_url = channel_name, channel_url
                                redirected_urls.append(new_url)
                        except Timeout:
                            new_url = f"timeout_{channel_name}", channel_url
                            redirected_urls.append(new_url)
                            print("请求超时")
                        except requests.RequestException as e:
                            new_url = f"error_{channel_name}", channel_url
                            redirected_urls.append(new_url)
                            print(f"请求发生错误: {e}")
                    else:
                        # 如果没有重定向，返回原始URL
                        new_url = channel_name, channel_url
                        redirected_urls.append(new_url)
                else:
                    redirected_urls.append(line)
            else:
                redirected_urls.append(line)
        except:
            print(line)
            
    return redirected_urls

# 示例用法
redirected_urls = get_redirected_urls(url_list)

with open("mywlkj_all_gt.txt", 'w', encoding='utf-8') as file:
    for line in redirected_urls:
        if len(line) > 0:
            parts = line.split()
            if len(parts) >= 2:
                name, name_url = parts 
                channel_url =(f"{name_url}")
                channel_url = channel_url.replace("https://gitee.com/tv2785/tvbox/raw/master/gg.mp4", "https://gitee.com/guoqi8899/ipvideo/raw/master/gg.mp4")
                file.write(f"{name},{channel_url}\n")
                print(line)
            else:
                file.write(f"{line}\n")
    file.close()
