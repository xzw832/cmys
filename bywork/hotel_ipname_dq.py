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

diqu = [
    "广西",
    "内蒙",
    "西藏",
    "天津",
    "北京",
    "重庆",
    "江苏",
    "香港",
    "青海",
    "甘肃",
    "陕西",
    "云南",
    "贵州",
    "四川",
    "海南",
    "广东",
    "湖南",
    "湖北",
    "河南",
    "山东",
    "江西",
    "福建",
    "安徽",
    "浙江",
    "黑龙江",
    "吉林",
    "辽宁",
    "山西",
    "河北",
    "上海",
    "台湾"
    ]
def contains_any_value(text, diqu):
    for dq in diqu:
        if dq in text:
            return dq
    return "未分类"
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
page = 250
urls = [
    "http://tonkiang.us/hoteliptv.php?page=1&s=江苏",
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

for i in range(1, page + 1):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        url = f"http://tonkiang.us/hoteliptv.php?page={i}&s=CCTV"
        print(url)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(90)  # 10秒后超时
        # 设置脚本执行超时
        driver.set_script_timeout(80)  # 5秒后超时
        # 使用WebDriver访问网页
        driver.get(url)  # 将网址替换为你要访问的网页地址
        WebDriverWait(driver, 75).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
        time.sleep(random.randint(3, 10))
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
            # print(result)
            html_txt = f"{result}"
            if "暂时失效" not in html_txt:
                m3u8_div = result.find("a")
                if m3u8_div:
                    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
                    urls_all = re.findall(pattern, m3u8_div.get('href'))
                    # print(urls_all)
                    if len(urls_all) > 0:
                        ip = urls_all[0]
                        italic_tags = soup.find_all('i')
                        # 尝试获取第二个<i>标签
                        if len(italic_tags) >= 1:
                            second_italic_tag = italic_tags[0]  # 索引从0开始，所以第二个标签的索引是1
                            url_name = second_italic_tag.text
                            name_html_txt = f"{url_name}"
                            name_html_txt = name_html_txt.replace(" ", "").replace("\n", "")
                            # print(html_txt)
                            # print("1===========================================================================================================")
                            if "移动" in html_txt:
                                ipname = '移动'
                            elif "移通" in html_txt:
                                ipname = '移动'
                            elif "视通" in html_txt:
                                ipname = '广电'
                            elif "联通" in html_txt:
                                ipname = '联通'
                            elif "电信" in html_txt:
                                ipname = '电信'
                            else:
                                ipname ='其他'
                            dq_name = contains_any_value(html_txt, diqu)
                            resultslist.append(f"{ipname},{ip},{dq_name}")
                            print(f"{ipname},{ip},{dq_name}")
                            name_html_txt = ""
    except:
        print(f"=========================>>> Thread {url} error")
        
resultslist = set(resultslist)    # 去重得到唯一的URL列表

with open("iplist.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.close()
sorted_list = sorted(resultslist)

def worker(thread_url,counter_id):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        #分离出运营商和IP
        in_name,in_url,dq_name = thread_url.split(',')
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=selenium{counter_id}")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=chrome_options)
        # 设置页面加载超时
        driver.set_page_load_timeout(60)  # 10秒后超时
     
        # 设置脚本执行超时
        driver.set_script_timeout(50)  # 5秒后超时
        # 使用WebDriver访问网页
        if is_odd_or_even(random.randint(1, 200)):
            page_url= f"http://tonkiang.us/9dlist2.php?s={in_url}"
        else:
            page_url= f"http://foodieguide.com/iptvsearch/alllist.php?s={in_url}"
        
        print(page_url)
        driver.get(page_url)  # 将网址替换为你要访问的网页地址
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tables_div = soup.find("div", class_="tables")
        results = (
            tables_div.find_all("div", class_="result")
            if tables_div
            else []
        )
        if not any(
            result.find("div", class_="m3u8") for result in results
        ):
            #break
            print("Err-------------------------------------------------------------------------------------------------------")
        for result in results:
            #print(result)
            m3u8_div = result.find("div", class_="m3u8")
            url_int = m3u8_div.text.strip() if m3u8_div else None
            #取频道名称
            m3u8_name_div = result.find("div", class_="channel")
            url_name = m3u8_name_div.text.strip() if m3u8_div else None
            #－－－－－
            #print("-------------------------------------------------------------------------------------------------------")
            name =f"{url_name}"
            if len(name) == 0:
                name = "Err画中画"
            #print(name)
            urlsp =f"{url_int}"
            if len(urlsp) == 0:
                urlsp = "rtp://127.0.0.1"             
            print(f"{dq_name}_{url_name}\t{url_int}")
            #print("-------------------------------------------------------------------------------------------------------")
            urlsp = urlsp.replace("http://67.211.73.118:9901", "")
            name = name.replace("cctv", "CCTV")
            name = name.replace("中央", "CCTV")
            name = name.replace("央视", "CCTV")
            name = name.replace("高清", "")
            name = name.replace("HD", "")
            name = name.replace("标清", "")
            name = name.replace("频道", "")
            name = name.replace("-", "")
            name = name.replace(" ", "")
            name = name.replace("PLUS", "+")
            name = name.replace("＋", "+")
            name = name.replace("(", "")
            name = name.replace(")", "")
            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
            name = name.replace("CCTV1综合", "CCTV1")
            name = name.replace("CCTV2财经", "CCTV2")
            name = name.replace("CCTV3综艺", "CCTV3")
            name = name.replace("CCTV4国际", "CCTV4")
            name = name.replace("CCTV4中文国际", "CCTV4")
            name = name.replace("CCTV4欧洲", "CCTV4")
            name = name.replace("CCTV5体育", "CCTV5")
            name = name.replace("CCTV6电影", "CCTV6")
            name = name.replace("CCTV7军事", "CCTV7")
            name = name.replace("CCTV7军农", "CCTV7")
            name = name.replace("CCTV7农业", "CCTV7")
            name = name.replace("CCTV7国防军事", "CCTV7")
            name = name.replace("CCTV8电视剧", "CCTV8")
            name = name.replace("CCTV9记录", "CCTV9")
            name = name.replace("CCTV9纪录", "CCTV9")
            name = name.replace("CCTV10科教", "CCTV10")
            name = name.replace("CCTV11戏曲", "CCTV11")
            name = name.replace("CCTV12社会与法", "CCTV12")
            name = name.replace("CCTV13新闻", "CCTV13")
            name = name.replace("CCTV新闻", "CCTV13")
            name = name.replace("CCTV14少儿", "CCTV14")
            name = name.replace("CCTV15音乐", "CCTV15")
            name = name.replace("CCTV16奥林匹克", "CCTV16")
            name = name.replace("CCTV17农业农村", "CCTV17")
            name = name.replace("CCTV17农业", "CCTV17")
            name = name.replace("CCTV5+体育赛视", "CCTV5+")
            name = name.replace("CCTV5+体育赛事", "CCTV5+")
            name = name.replace("CCTV5+体育", "CCTV5+")
            name = name.replace("CMIPTV", "")
            name = name.replace("内蒙卫视", "内蒙古卫视")
            name = name.replace("CCTVCCTV", "CCTV")
            if "http" in urlsp:
                # 获取锁
                lock.acquire()
                infoList.append(f"{name}_{in_name}_{dq_name},{urlsp}")
                # 释放锁
                lock.release()
        print(f"=========================>>> Thread {in_url} save ok")
    except Exception as e:
        print(f"=========================>>> Thread {in_url} caught an exception: {e}")
    finally:
        # 确保线程结束时关闭WebDriver实例
        driver.quit() 
        print(f"=========================>>> Thread {in_url}  quiting")
        # 标记任务完成
        time.sleep(0)

# 创建一个线程池，限制最大线程数为3
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # 提交任务到线程池，并传入参数
    counter = increment_counter()
    for i in sorted_list:  # 假设有5个任务需要执行
        executor.submit(worker, i ,counter)

infoList = set(infoList)  # 去重得到唯一的URL列表
infoList = sorted(infoList)

with open("myitv.txt", 'w', encoding='utf-8') as file:
    for info in infoList:
        file.write(info + "\n")
        print(info)
    file.close()
