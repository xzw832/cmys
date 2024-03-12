import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
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
                name = name.replace("_", "")
                name = name.replace("HD", "")
                name = name.replace("(高清)", "")
                name = name.replace("厦门卫视高清", "厦门卫视")
                name = name.replace("吉林卫视高清", "吉林卫视")
                name = name.replace("四川卫视高清", "四川卫视")
                name = name.replace("天津卫视高清", "天津卫视")
                name = name.replace("天津高清", "天津卫视")
                name = name.replace("安徽卫视高清", "安徽卫视")
                name = name.replace("广东卫视高清", "广东卫视")
                name = name.replace("江苏卫视高清", "江苏卫视")
                name = name.replace("河北卫视高清", "河北卫视")
                name = name.replace("浙江卫视高清", "浙江卫视")
                name = name.replace("深圳卫视高清", "深圳卫视")
                name = name.replace("湖北卫视高清", "湖北卫视")
                name = name.replace("湖南卫视高清", "湖南卫视")
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
                name = name.replace("福建东南卫视", "东南卫视")
                name = name.replace("汕头综合高清", "汕头综合")
                name = name.replace("汕头文旅体育高清", "汕头文旅体育")
                name = name.replace("汕头文旅体育高清", "汕头文旅体育")
                name = name.replace("高清", "")
                urlright = channel_url[:4]
                if urlright == 'http'
                    results.append(f"{name},{channel_url}")
    file.close()

results = set(results)  # 去重得到唯一的URL列表
results = sorted(results)

with open("itv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        # print(result)
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
                if 'CCTV' in channel_name:
                    channels.append((channel_name, channel_url))
    file.close()
# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        now=time.time()
        try:
            res=se.get(i,headers=headers,timeout=5,stream=True)
            if res.status_code==200:
                for k in res.iter_content(chunk_size=1048576):
                    # 这里的chunk_size是1MB，每次读取1MB测试视频流
                    # 如果能获取视频流，则输出读取的时间以及链接
                    if k:
                        print(f'{time.time()-now:.2f}\t{i}')
                        response_time = (time.time()-now) * 1
                        download_speed = 1048576 / response_time / 1024
                        normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                        result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                        results.append(result)
                        break
        except:
            # 无法连接并超时的情况下输出“X”
            print(f'X\t{i}')
        
        # 减少CPU占用
        time.sleep(0)
        # 标记任务完成
        task_queue.task_done()


# 创建多个工作线程
num_threads = 15
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
    
result_counter = 8  # 每个频道需要的个数

with open("cctv.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  央视频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
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
