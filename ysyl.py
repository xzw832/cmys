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

with open("itv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if '电影' in channel_name or '影院' in channel_name or '剧场' in channel_name or '影视' in channel_name:
                    channels.append((channel_name, channel_url))
    file.close()
# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            now=time.time()
            res=se.get(channel_url,headers=headers,timeout=5,stream=True)
            if res.status_code==200:
                for k in res.iter_content(chunk_size=1048576):
                    # 这里的chunk_size是1MB，每次读取1MB测试视频流
                    # 如果能获取视频流，则输出读取的时间以及链接
                    if k:
                        print(f'{time.time()-now:.2f}\t{channel_url}')
                        response_time = (time.time()-now) * 1
                        download_speed = 1048576 / response_time / 1024
                        normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                        result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                        results.append(result)
                        break
        except:
            # 无法连接并超时的情况下输出“X”
            print(f'X\t{channel_url}')
        
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
#results.sort(key=lambda x: channel_key(x[0]))
now_today = datetime.date.today()
# 将结果写入文件

result_counter = 8  # 每个频道需要的个数

with open("ysyl.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  影视频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '电影' in channel_name or '影院' in channel_name or '剧场' in channel_name or '影视' in channel_name:
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
