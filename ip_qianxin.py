import subprocess
import concurrent.futures
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
results = []
for line in flattened_list:
    try:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                result = channel_name, channel_url, "0.001 MB/s"
                results.append(result)
flattened_list = set(results)
# 测试分辨率
def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_name,width,height,r_frame_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=20, text=True)
        output = result.stdout
        # print(output)
        # 使用正则表达式匹配并提取信息
        pattern = r'^(h264)\s+(\d+)\s+(\d+)\s+(\d+/\d+)?$'
        matches = re.findall(pattern, output, re.MULTILINE)
        
        if matches:
            codec_name, width, height, r_frame_rate = matches[0]
            return codec_name, int(width), int(height), int(eval(r_frame_rate))
        else:
            raise ValueError("No valid matches found in ffprobe output.")
    
    except subprocess.CalledProcessError as e:
        return f"ffprobe command failed with error: {e}"
    except subprocess.TimeoutExpired:
        return "ffprobe command timed out."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def process_video(video_url):
    channel_name, channel_url, speed = video_url
    try:
        codec_name, width, height, r_frame_rate = check_video_source_with_ffmpeg(channel_url)
        return (codec_name, width, height, r_frame_rate)
    except ValueError as e:
        print(f"Error parsing ffprobe output for {video_url}: {e}")
        return (None, None, None, None)
    except Exception as e:
        print(f"An error occurred for {video_url}: {e}")
        return (None, None, None, None)

# 最大线程数
max_workers = 50
video_urls = set(results)
results = []
# 使用ThreadPoolExecutor创建线程池
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # 提交任务到线程池
    future_to_url = {executor.submit(process_video, url): url for url in video_urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            # 获取任务返回的结果（分辨率和码率）
            resolution_and_bitrate = future.result()
            # 处理或记录结果
            print(f"Results for {url}: {resolution_and_bitrate}")
            codec_name, width, height, r_frame_rate = resolution_and_bitrate
            if codec_name == 'h264' and width >= 720 and r_frame_rate < 50:
                results.append(url)
        except Exception as exc:
            print(f'{url} generated an exception: {exc}')

flattened_list = sorted(results)
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

        
