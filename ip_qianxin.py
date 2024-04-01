import os
import re
import base64
import requests
import chardet
import json
import time
import random

# 从环境变量中获取API密钥和基础URL
api_key = "f2c0a15a6c33c43418b37a7027d99b739a38b6bace593b176e0c459a572808b2"
base_url = "https://hunter.qianxin.com/openApi/search"
flattened_list = []
# 配置信息
spider_cfg = {
    'apiKey': api_key,
    'baseUrl': base_url,
    'search': 'web.body="dbiptv.sn.chinamobile.com" && ip.country=="中国"',
    'page': 2,
    'pageSize': 50,
}
url_list = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
se = requests.Session()

def analysis_m3u(data):
    items = data.split("\n")
    items = [item for item in items if item.strip()]

    item_info = None
    list_data = []

    for item in items:
        item = item.strip()

        if item.startswith("#EXTM3U"):
            continue

        if item.startswith("#EXTINF"):
            item_info = None

            id_match = re.search(r'tvg-id="(.*?)"', item)
            name_match = re.search(r'tvg-name="(.*?)"', item)
            logo_match = re.search(r'tvg-logo="(.*?)"', item)
            group_match = re.search(r'group-title="(.*?)"', item)

            id = id_match.group(1) if id_match else None
            name = name_match.group(1) if name_match else None
            logo = logo_match.group(1) if logo_match else None
            group = group_match.group(1) if group_match else None

            channel_name = item.split(",")[-1].strip() if "," in item else None

            item_info = {
                'id': id,
                'name': name,
                'logo': logo,
                'group': group,
                'channelName': channel_name,
                'originLine': item,
                'itemTag': "#EXTINF",
            }

            continue
        elif len(item) > 0:
            count = item.count(',')
            if count == 0:
                channel_url = item
                
        # Assuming you want to append item_info to list_data when it's not null
        if item_info:
            item_info = f"{channel_name},{channel_url}"
            flattened_list.append(item_info)

    return list_data

def analysis_txt(data):
    items = data.split("\r\n")
    items = [item for item in items if item.strip()]

    list_data = []

    for item in items:
        count = item.count(',')
        if count == 1:
            title, url = item.split(",")  # Limit split to first comma
            is_url = any(url.startswith(key) for key in ["http://", "https://"])
    
            if title and url and is_url:
                channel_name = title.strip()
                channel_url = url.strip()
                item_info = f"{channel_name},{channel_url}"
                flattened_list.append(item_info)
    return list_data

def analysis_json(json_data):
    data = json.loads(json_data)
    for item in data['lives']:
        # 遍历"channels"列表
        for sub_item in item['channels']:
            # 获取"name"和"urls"列表
            name = sub_item['name']
            urls = sub_item['urls']
            # 遍历"urls"列表，将"name"和每个"url"组合成字符串，并添加到结果列表中
            for url in urls:
                flattened_list.append(f"{name},{url}")

def get_target_list(page):
    try:
        # 构建API URL
        search_encoded = base64.b64encode(spider_cfg['search'].encode()).decode()
        url = f"{spider_cfg['baseUrl']}?api-key={spider_cfg['apiKey']}&search={search_encoded}&page={page}&page_size={spider_cfg['pageSize']}"
        print(url)
        # 发送GET请求
        response = requests.get(url)
        
        # 检查响应状态码
        if response.status_code == 200:
            print(response.text)
            # 假设响应的JSON结构与原始Node.js代码中的结构相同
            data = response.json().get('data', {}).get('arr', [])
            return [item['url'] for item in data] if data else []
        else:
            return []
    except Exception as e:
        print(f"获取目标列表时发生错误: {e}")
        return []
for i in range(1, spider_cfg['page'] + 1):
    item = get_target_list(i)
    for lin in item:
        print("--------------------------------->>>>>>>>>>>>>>>>>", lin)
        try:
            response = se.get(lin, headers=headers, timeout=10)
            if response.status_code == 200:
                detected_encoding = chardet.detect(response.content)['encoding']
                if detected_encoding is not None:
                    content = response.content.decode(detected_encoding, errors='ignore')
                else:
                    # 你可以选择一个默认的编码，或者记录一个错误，或者采取其他措施
                    content = response.content.decode('utf-8', errors='ignore')
                print(content)
                if content.startswith("#EXTM3U"):
                    url_list.append(analysis_m3u(content))  # 使用content而不是data
                elif content.startswith('{"lives"'):
                    analysis_json(content)
                elif content.startswith('{"spider"'):
                    analysis_json(content)
                else:
                    url_list.append(analysis_txt(content))  # 使用content而不是data
        except requests.RequestException as e:
            # 更具体地捕获请求异常
            print(f'无法连接并超时----------------------->\t{lin}\nError: {e}')
            continue
        time.sleep(5)
flattened_list = set(flattened_list)
flattened_list = sorted(flattened_list)
with open("ip_qianxin.txt", 'w', encoding='utf-8') as file:
    for line in flattened_list:
        try:
            line = line.strip()
            count = line.count(',')
            if count == 1:
                if line:
                    channel_name, channel_url = line.split(',')
                    file.write(f"{channel_name},{channel_url}\n")
        except:
            print(f'错误----------------------->\t{line}')
            continue

        
