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
    "http://tonkiang.us/hoteliptv.php?page=1&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=2&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=3&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=4&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=5&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=6&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=7&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=8&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=9&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=10&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=11&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=12&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=13&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=14&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=15&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=16&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=17&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=18&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=19&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=20&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=21&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=22&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=23&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=24&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=25&s=江苏",
    "http://tonkiang.us/hoteliptv.php?page=1&s=东海新闻",
    "http://tonkiang.us/hoteliptv.php?page=1&s=南京",
    "http://tonkiang.us/hoteliptv.php?page=1&s=响水",
    "http://tonkiang.us/hoteliptv.php?page=1&s=宿迁",
    "http://tonkiang.us/hoteliptv.php?page=1&s=常州",
    "http://tonkiang.us/hoteliptv.php?page=1&s=徐州",
    "http://tonkiang.us/hoteliptv.php?page=1&s=江苏体育",
    "http://tonkiang.us/hoteliptv.php?page=1&s=沛县",
    "http://tonkiang.us/hoteliptv.php?page=1&s=泗洪",
    "http://tonkiang.us/hoteliptv.php?page=1&s=泰州",
    "http://tonkiang.us/hoteliptv.php?page=1&s=淮安",
    "http://tonkiang.us/hoteliptv.php?page=1&s=睢宁",
    "http://tonkiang.us/hoteliptv.php?page=1&s=赣榆",
    "http://tonkiang.us/hoteliptv.php?page=1&s=连云",
    "http://tonkiang.us/hoteliptv.php?page=1&s=高淳"
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

for url in urls:
    # 创建一个Chrome WebDriver实例
    results = []
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
    WebDriverWait(driver, 45).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.tables")
            )
    )
    time.sleep(20)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 关闭WebDriver
    driver.quit()
    tables_div = soup.find("div", class_="tables")
    results = (
        tables_div.find_all("div", class_="result")
        if tables_div
        else []
    )
    if not any(
        result.find("div", class_="channel") for result in results
    ):
        #break
        print("Err-------------------------------------------------------------------------------------------------------")
    for result in results:
        print("============================================================================================================")
        print(result)
        html_txt = f"{result}"
        # print(html_txt)
        if "result" in html_txt:
            m3u8_div = result.find("a")
            if m3u8_div:
                pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
                urls_all = re.findall(pattern, m3u8_div.get('href'))
                # print(urls_all)
                if len(urls_all) > 0:
                    ip = urls_all[0]
                    italic_tags = soup.find_all('i')
                    # 尝试获取第二个<i>标签
                    if len(italic_tags) > 1:
                        second_italic_tag = italic_tags[1]  # 索引从0开始，所以第二个标签的索引是1
                        url_name = second_italic_tag.text
                        name_html_txt = f"{url_name}"
                        if "移动" in name_html_txt:
                            ipname = '移动'
                        elif "联通" in name_html_txt:
                            ipname = '联通'
                        elif "电信" in name_html_txt:
                            ipname = '电信'
                        else:
                            ipname ='其他'
                        resultslist.append(f"{ipname},{ip}")

resultslist = set(resultslist)    # 去重得到唯一的URL列表

with open("pingdao.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.close()
sorted_list = sorted(resultslist)
