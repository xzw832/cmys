import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()
# 判断首位是否为数字，是返回真
def is_first_digit(s):
    return s[0].isdigit() if s else False
    
# 线程安全的队列，用于存储下载任务
task_queue = Queue()
lock = threading.Lock()
# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
headers={'User-Agent': 'okhttp/3.15 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
se=requests.Session()

with open("myitv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                name =(f"{channel_name}")
                name = name.replace("[", "")
                name = name.replace("]", "")
                name = name.replace("HD", "")
                name = name.replace("(", "")
                name = name.replace(")", "")
                name = name.replace("天津高清", "天津卫视高清")
                name = name.replace("广东高清", "广东卫视高清")
                name = name.replace("深圳高清", "深圳卫视高清")
                name = name.replace("湖北高清", "湖北卫视高清")
                name = name.replace("湖南高清", "湖南卫视高清")
                name = name.replace("福建东南卫视高清", "东南卫视高清")
                name = name.replace("山东教育", "山东教育卫视")
                name = name.replace("山东高清", "山东卫视高清")
                name = name.replace("广东体育高清", "广东体育卫视高清")
                name = name.replace("广东珠江高清", "广东珠江卫视高清")
                name = name.replace("广东高清", "广东卫视高清")
                name = name.replace("浙江高清", "浙江卫视高清")
                name = name.replace("深圳高清", "深圳卫视高清")
                name = name.replace("湖北高清", "湖北卫视高清")
                name = name.replace("湖南高清", "湖南卫视高清")
                name = name.replace("江苏高清", "江苏卫视高清")
                name = name.replace("北京卫视高清", "北京卫视高清")
                name = name.replace("北京高清", "北京卫视高清")
                name = name.replace("福建东南卫视", "东南卫视")
                name = name.replace("凤凰中文", "凤凰卫视中文")
                name = name.replace("凤凰资讯", "凤凰卫视资讯")
                name = name.replace("凤凰香港", "凤凰香港卫视")
                name = name.replace("本港", "本港卫视")
                name = name.replace("香港明珠", "香港明珠卫视")
                name = name.replace("香港翡翠", "香港翡翠卫视")
                name = name.replace("香港音乐", "香港音乐卫视")
                name = name.replace("高请", "高清")
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
                name = name.replace("CCTV4K4K50p", "CCTV4K50p")
                name = name.replace("CCTV4K4K", "CCTV4K")
                name = name.replace("BRTV北京卫视", "北京卫视")
                urlright = channel_url[:4]
                if urlright == 'http':
                    if '画中画' not in channel_name and '单音' not in channel_name and '直播' not in channel_name and '测试' not in channel_name and '主视' not in channel_name:
                        check_name = f"{name}"
                        if not is_first_digit(check_name):
                            results.append(f"{name},{channel_url}")
    file.close()

results = set(results)  # 去重得到唯一的URL列表
# results = sorted(results)

with open("newitv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        # print(result)
    file.close()

# 合并文件内容
file_contents = []
file_paths = ["cctv.txt", "weishi.txt", "ktpd.txt", "ysyl.txt","xiangang.txt", "qita.txt", "newitv.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
        file.close()

# print(f"{now_today}合并文件完成")
# 写入合并后的文件
with open("itv.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    output.close()

results = []
with open("itv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                results.append(f"{channel_name},{channel_url}")
                
results = set(results)  # 去重得到唯一的URL列表
# results = sorted(results)
with open("itv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url = result.split(',')
        file.write(f"{channel_name},{channel_url}\n")
    file.close()

results = []
channels = []
with open("itv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if 'CCTV' in channel_name or 'CETV' in channel_name or 'CQTV' in channel_name or 'IPTV' in channel_name:
                    channels.append((channel_name, channel_url))
    file.close()
# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        if ".m3u8" in channel_url or ".flv" in channel_url or ".mp4" in channel_url:
            try:
                channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
                lines = requests.get(channel_url,headers=headers, timeout=3, stream=True).text.strip().split('\n')  # 获取m3u8文件内容
                ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
                ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
                ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接
    
                # 多获取的视频数据进行5秒钟限制
                with eventlet.Timeout(5, False):
                    start_time = time.time()
                    content = requests.get(ts_url,headers=headers, timeout=(2,5), stream=True).content
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1
    
                if content:
                    with open(ts_lists_0, 'ab') as f:
                        f.write(content)  # 写入文件
                    file_size = len(content)
                    # print(f"文件大小：{file_size} 字节")
                    download_speed = file_size / response_time / 1178
                    # print(f"下载速度：{download_speed:.3f} kB/s")
                    normalized_speed = min(max(download_speed / 1178, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                    #print(f'{channel_url}')
                    #print(f"m3u8 标准化后的速率：{normalized_speed:.3f} MB/s")
    
                    # 删除下载的文件
                    os.remove(ts_lists_0)
                    result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                    # 获取锁
                    lock.acquire()
                    results.append(result)
                    # 释放锁
                    lock.release()
                    numberx = (len(results) + len(error_channels)) / len(channels) * 100
                    # print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
            except:
                error_channel = channel_name, channel_url
                # error_channels.append(error_channel)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
        else:
            try:
                now=time.time()
                res=se.get(channel_url,headers=headers,stream=True,timeout=5)
                if res.status_code==200:
                    for k in res.iter_content(chunk_size=2097152):
                        # 这里的chunk_size是1MB，每次读取1MB测试视频流
                        # 如果能获取视频流，则输出读取的时间以及链接
                        if time.time()-now > 15:
                            res.close()
                            print(f'Time out\t{channel_url}')
                            break
                        else:
                            if k:
                                print(f'{time.time()-now:.2f}\t{channel_url}')
                                response_time = (time.time()-now) * 1
                                download_speed = 2097152 / response_time / 1024
                                normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                                if response_time > 1.2:
                                    result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                                    # 获取锁
                                    lock.acquire()
                                    results.append(result)
                                    # 释放锁
                                    lock.release()
                                else:
                                    print(f'X\t{channel_url}')
                                break
            except:
                # 无法连接并超时的情况下输出“X”
                print(f'X\t{channel_url}')
        
        # 减少CPU占用
        time.sleep(0)
        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 40
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True) 
    #t = threading.Thread(target=worker, args=(event,len(channels)))  # 将工作线程设置为守护线程
    t.start()
    #event.set()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()

# 打开移动源文件
with open("chinamobile.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if 'CCTV' in channel_name:
                    result = channel_name, channel_url, "0.001 MB/s"
                    results.append(result)
                    
def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))
now_today = datetime.date.today()

# 将结果写入文件
with open("cctv_all_results.txt", 'w', encoding='utf-8') as file:
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url},{speed}\n")
    file.close()
    
result_counter = 16  # 每个频道需要的个数

with open("cctv.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  央视频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name or 'CETV' in channel_name or 'CQTV' in channel_name or 'IPTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

    file.close()
