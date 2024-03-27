import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()

lock = threading.Lock()
now_today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
# 线程安全的队列，用于存储下载任务
task_queue = Queue()
lock = threading.Lock()
results = []
channels = []
error_channels = []
headers={'User-Agent': 'okhttp/3.12.10(Linux;Android9;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36'}
se=requests.Session()

def cut_first_chinese_words(text, num=2):
    for i, char in enumerate(text):
        if char >= '\u4e00' and char <= '\u9fa5':
            return text[:i+2]
    return 'xxxxxxxxxxxxxxxxxx'
    
#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

urls = [
    "东海新闻,http://49.75.132.37:4022/rtp/239.49.1.158:6000",
    "南京娱乐,http://110.85.30.16:4022/rtp/239.61.3.60:9878",
    "CCTV1,http://61.52.156.194:808/hls/1/index.m3u8",
    ]

def modify_urls(http_url):
    channel,url = http_url.split(',')
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find("/", ip_start_index)  # 查找下一个"/"的位置，用来确定IP地址的结束位置
    
    # 提取IP地址
    if ip_end_index != -1:
        ip_address = url[ip_start_index:ip_end_index]
    else:
        # 如果没有找到下一个"/"，则假设URL的末尾就是IP地址的结束位置
        ip_address = url[ip_start_index:]
    # 分割IP地址和端口
    new_ip_address, port = ip_address.split(':')
    # 分割IP地址的各个部分
    new_ip_address = new_ip_address.split('.')
    # 把尾位（最后一个部分）变成1
    new_ip_address[-1] = '1'
    # 重新组合IP地址的各个部分
    ip_address = '.'.join(new_ip_address)
    ip_start = url[:ip_start_index]
    ip_end = url[ip_end_index:]
    for i in range(1, 255):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{channel},{ip_start}{modified_ip}:{port}{ip_end}"
        print(modified_url)
        channels.append((channel, modified_url))

def is_url_accessible(url):
    try:
        return url
    except requests.exceptions.RequestException:
        pass
    # return None
    return url
# 初始化计数器为0
counter = -1
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

valid_urls = []
#   多线程获取可用url
for ipv in urls:
    url = ipv.strip()
    modify_urls(url)

# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        if "m3u8" in channel_url or "flv" in channel_url:
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
                    results.append(result)
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
                        if time.time()-now > 30:
                            res.close()
                            print(f'Time out\t{channel_url}')
                            break
                        else:
                            if k:
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

result_counter = 16  # 每个频道需要的个数

with open("seekip_ok.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    for result in results:
        channel_name, channel_url, speed = result
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

print(f"{now_today}ip测试完成")
