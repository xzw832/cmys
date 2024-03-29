import requests
from requests.exceptions import Timeout

load_urls = [
    "http://mywlkj.ddns.net:754/tv.php",
    ]
file_contents = []
for url in load_urls:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        print(response.text)
        file_contents.append(response.text)
url_list = [line for line_str in file_contents for line in line_str.split('\n')]
for result in url_list:
    print(result)
    
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
                    if '#' not in channel_url:
                        try:
                            response = requests.head(channel_url, allow_redirects=False, timeout=3.0)
                            # 如果初始请求返回200，但之后服务器又发出了302重定向，我们需要处理这种情况
                            if response.status_code == 200 and 'Location' in response.headers:
                                redirected_url = response.headers['Location']
                                redirected_response = session.head(redirected_url)
                                new_url = channel_name, redirected_response.url
                                redirected_urls.append(new_url)
                            # 如果初始请求直接返回了重定向，我们直接返回重定向的URL
                            elif response.status_code in [301, 302, 303, 307, 308]:
                                print("--------------------",response.headers['Location'])
                                new_url = channel_name, response.headers['Location']
                                redirected_urls.append(new_url)
                            else:
                                # 如果没有重定向，返回原始URL
                                new_url = channel_name, channel_url
                                redirected_urls.append(new_url)
                        except Timeout:
                            print("请求超时")
                        except requests.RequestException as e:
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

with open("mywlkj_all.txt", 'w', encoding='utf-8') as file:
    for line in redirected_urls:
        name, name_url = line
        channel_url =(f"{name_url}")
        channel_url = channel_url.replace("https://gitee.com/tv2785/tvbox/raw/master/gg.mp4", "https://gitee.com/guoqi8899/ipvideo/raw/master/gg.mp4")
        file.write(f"{name},{channel_url}\n")
        print(line)
    file.close()
