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
    
# with open("iptv_all.txt", "w", encoding="utf-8") as output:
#    output.write('\n'.join(file_contents))
#    output.close()

results = []
with open("iptv_all.txt", 'r', encoding='utf-8') as file:
    lines = file_contents.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                name =(f"{channel_name}")
                name = name.replace("「新疆」", "")
                name = name.replace("「代理」", "")
                name = name.replace("「IPV6」", "")
                name = name.replace("「移动」", "")
                name = name.replace("「官方」", "")
                name = name.replace("「电信」", "")
                name = name.replace("「联通」", "")
                name = name.replace("「河北有线」", "")
                name = name.replace("「北方广电」", "")
                name = name.replace("「辽宁联通」", "")
                name = name.replace("1920*1080", "")
                name = name.replace("_", "")
                name = name.replace("[", "")
                name = name.replace("]", "")
                name = name.replace("HD", "")
                name = name.replace("(高清)", "")
                name = name.replace("超清", "")
                name = name.replace("厦门卫视高清", "厦门卫视")
                name = name.replace("吉林卫视高清", "吉林卫视")
                name = name.replace("四川卫视高清", "四川卫视")
                name = name.replace("天津卫视高清", "天津卫视")
                name = name.replace("天津高清", "天津卫视")
                name = name.replace("安徽卫视高清", "安徽卫视")
                name = name.replace("广东卫视高清", "广东卫视")
                name = name.replace("广东高清", "广东卫视")
                name = name.replace("江苏卫视高清", "江苏卫视")
                name = name.replace("河北卫视高清", "河北卫视")
                name = name.replace("浙江卫视高清", "浙江卫视")
                name = name.replace("深圳高清", "深圳卫视")
                name = name.replace("深圳卫视高清", "深圳卫视")
                name = name.replace("湖北卫视高清", "湖北卫视")
                name = name.replace("湖北高清", "湖北卫视")
                name = name.replace("湖南卫视高清", "湖南卫视")
                name = name.replace("湖南高清", "湖南卫视")
                name = name.replace("福建东南卫视高清", "福建东南卫视")
                name = name.replace("辽宁卫视高清", "辽宁卫视")
                name = name.replace("黑龙江卫视高清", "黑龙江卫视")
                name = name.replace("山东教育", "山东教育卫视")
                name = name.replace("山东高清", "山东卫视")
                name = name.replace("广东体育高清", "广东体育卫视")
                name = name.replace("广东珠江高清", "广东珠江卫视")
                name = name.replace("广东高清", "广东卫视")
                name = name.replace("浙江高清", "浙江卫视")
                name = name.replace("深圳高清", "深圳卫视")
                name = name.replace("湖北高清", "湖北卫视")
                name = name.replace("湖南高清", "湖南卫视")
                name = name.replace("江苏高清", "江苏卫视")
                name = name.replace("北京卫视高清", "北京卫视")
                name = name.replace("北京高清", "北京卫视")
                name = name.replace("福建东南卫视", "东南卫视")
                name = name.replace("汕头综合高清", "汕头综合")
                name = name.replace("汕头文旅体育高清", "汕头文旅体育")
                name = name.replace("汕头文旅体育高清", "汕头文旅体育")
                name = name.replace("高清", "")
                name = name.replace("凤凰中文", "凤凰卫视中文")
                name = name.replace("凤凰资讯", "凤凰卫视资讯")
                name = name.replace("凤凰香港", "凤凰香港卫视")
                name = name.replace("本港", "本港卫视")
                name = name.replace("香港明珠", "香港明珠卫视")
                name = name.replace("香港翡翠", "香港翡翠卫视")
                name = name.replace("香港音乐", "香港音乐卫视")
                name = name.replace("高请", "")
                name = name.replace("超", "")
                name = name.replace("CCTVCCTV", "CCTV")
                name = name.replace("汕头二台", "汕头经济生活")
                name = name.replace("汕头二", "汕头经济生活")
                name = name.replace("汕头一台", "汕头综合")
                name = name.replace("汕头一", "汕头综合")
                name = name.replace("汕头三台", "汕头文旅体育")
                name = name.replace("汕头台", "汕头综合")
                name = name.replace("汕头生活", "汕头经济生活")
                name = name.replace("汕头文化", "汕头文旅体育")
                name = name.replace("揭西台", "揭西")
                name = name.replace("揭阳台", "揭阳综合")
                name = name.replace("风云音乐", "音乐风云")
                name = name.replace("东莞综合", "东莞新闻综合")
                name = name.replace("东莞资讯", "东莞生活资讯")
                name = name.replace("凤凰卫视资讯台", "凤凰卫视资讯")
                name = name.replace("山东教育卫视卫视", "山东教育卫视")
                name = name.replace("黑龙江卫视清", "黑龙江卫视")
                name = name.replace("CCTV4K4K50p", "CCTV4K50p")
                name = name.replace("CCTV4K4K", "CCTV4K")
                name = name.replace("BRTV北京卫视", "北京卫视")
                urlright = channel_url[:4]
                if urlright == 'http':
                    if "[" not in channel_url and "#genre#" not in channel_url:
                        if '画中画' not in channel_name and '单音' not in channel_name and '直播' not in channel_name and '测试' not in channel_name and '主视' not in channel_name:
                            check_name = f"{name}"
                            if not is_first_digit(check_name):
                                results.append(f"{name},{channel_url}")

    results = set(results)  # 去重得到唯一的URL列表
    results = sorted(results)
    for result in results:
        file.write(result + "\n")
        # print(result)
    file.close()
