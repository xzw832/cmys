import time
import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re

urls = [
    "http://tonkiang.us/hoteliptv.php?page=1&s=%E5%87%A4%E5%87%B0"
    ]

results = []

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=chrome_options)
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(10)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()

    # 查找所有符合指定格式的网址
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls = set(urls_all)  # 去重得到唯一的URL列表
    for url in urls:
      print(url)

infoList = []
for url in urls:
    try:
        page_url = f"http://tonkiang.us/9dlist2.php?s={url}"
        self.driver.get(page_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
            )
        )
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        tables_div = soup.find("div", class_="tables")
        results = (
            tables_div.find_all("div", class_="result")
            if tables_div
            else []
        )
        if not any(
            result.find("div", class_="m3u8") for result in results
        ):
            break
        for result in results:
            m3u8_div = result.find("div", class_="m3u8")
            url_int = m3u8_div.text.strip() if m3u8_div else None
            info_div = (
                m3u8_div.find_next_sibling("div") if m3u8_div else None
            )
            resolution = None
            if info_div:
                info_text = info_div.text.strip()
                resolution = (
                    info_text.partition(" ")[2].partition("•")[2]
                    if info_text.partition(" ")[2].partition("•")[2]
                    else None
                )
            infoList.append((url_int, resolution))
    except Exception as e:
        print(f"Error on page {page}: {e}")
        continue

for info in infoList:
    print(info)
