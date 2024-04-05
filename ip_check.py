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
lock = threading.Lock()
# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
headers={'User-Agent': 'okhttp/3.12.10(Linux;Android9;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36'}
se=requests.Session()

with open("cfg_ip.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if 'http' in channel_url:
                    channels.append((channel_name, channel_url))

    file.close()
channels = set(channels)
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
                    content = requests.get(ts_url,headers=headers, timeout=(1,4), stream=True).content
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1
                if content:
                    with open(ts_lists_0, 'ab') as f:
                        f.write(content)  # 写入文件
                    file_size = len(content)
                    # print(f"文件大小：{file_size} 字节")
                    download_speed = file_size / response_time / 1024
                    # print(f"下载速度：{download_speed:.3f} kB/s")
                    normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                    #print(f'{channel_url}')
                    print(f"m3u8 标准化后的速率：{normalized_speed:.3f} MB/s {channel_url}")
    
                    # 删除下载的文件
                    os.remove(ts_lists_0)
                    result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                    # 获取锁
                    lock.acquire() 
                    if normalized_speed > 0.001:
                        results.append(result)
                    else:
                        error_channel = channel_name, channel_url
                        error_channels.append(error_channel)
                    # 释放锁
                    lock.release()
                    
                    numberx = (len(results) + len(error_channels)) / len(channels) * 100
                    # print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
            except:
                error_channel = channel_name, channel_url
                # 获取锁
                lock.acquire()
                error_channels.append(error_channel)
                # 释放锁
                lock.release()
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
        else:
            try:
                now=time.time()
                res=se.get(channel_url,headers=headers,timeout=5,stream=True)
                if res.status_code==200:
                    for k in res.iter_content(chunk_size=2097152):
                        # 这里的chunk_size是1MB，每次读取1MB测试视频流
                        # 如果能获取视频流，则输出读取的时间以及链接
                        if time.time()-now > 60:
                            res.close()
                            print(f'Time out\t{channel_url}')
                            error_channel = channel_name, channel_url
                            # 获取锁
                            lock.acquire()
                            error_channels.append(error_channel)
                            # 释放锁
                            lock.release()
                            break
                        else:
                            if k:    # 检查是否有内容
                                print(f'{time.time()-now:.2f}\t{channel_url}')
                                response_time = (time.time()-now) * 1
                                download_speed = 2097152 / response_time / 1024
                                normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                                if response_time > 1:
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
                error_channel = channel_name, channel_url
                # 获取锁
                lock.acquire()
                error_channels.append(error_channel)
                # 释放锁
                lock.release()
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

now_today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 将结果写入文件
with open("cfg_ip.txt", 'w', encoding='utf-8') as file:
    file.write('失效连接,#genre#\n')
    for result in error_channels:
        channel_name, channel_url = result
        file.write(f"{channel_name},{channel_url}\n")

    file.write('有效连接,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        file.write(f"{channel_name},{channel_url}\n")
    file.write(f"测试完成时间,{now_today}\n")
    file.close()
