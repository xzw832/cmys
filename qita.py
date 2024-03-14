import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()

def cut_first_chinese_words(text, num=2):
    for i, char in enumerate(text):
        if char >= '\u4e00' and char <= '\u9fa5':
            return text[:i+2]
    return 'xxxxxxxxxxxxxxxxxx'

guangdong_text = "东莞中山佛山顺德南海南方宝安岭南广东广州广视揭西揭阳汕头汕尾江门海豚深圳清远龙岗湛江潮州珠江粤语肇庆茂名韶关"

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
se=requests.Session()

with open("itv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
                    channels.append((channel_name, channel_url))
    file.close()
# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        if "m3u8" in channel_url or "flv" in channel_url:
            try:
                channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
                lines = requests.get(channel_url, timeout=3, stream=True).text.strip().split('\n')  # 获取m3u8文件内容
                ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
                ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
                ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接
    
                # 多获取的视频数据进行5秒钟限制
                with eventlet.Timeout(5, False):
                    start_time = time.time()
                    content = requests.get(ts_url, timeout=(1,4), stream=True).content
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1
    
                if content:
                    with open(ts_lists_0, 'ab') as f:
                        f.write(content)  # 写入文件
                    file_size = len(content)
                    # print(f"文件大小：{file_size} 字节")
                    download_speed = file_size / response_time / 1024
                    print(f"下载速度：{download_speed:.3f} kB/s")
                    normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                    #print(f'{channel_url}')
                    #print(f"m3u8 标准化后的速率：{normalized_speed:.3f} MB/s")
    
                    # 删除下载的文件
                    os.remove(ts_lists_0)
                    result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                    results.append(result)
                    numberx = (len(results) + len(error_channels)) / len(channels) * 100
                    # print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
            except:
                error_channel = channel_name, channel_url
                error_channels.append(error_channel)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
        else:
            try:
                now=time.time()
                res=se.get(channel_url,headers=headers,timeout=5,stream=True)
                if res.status_code==200:
                    for k in res.iter_content(chunk_size=3145728):
                        # 这里的chunk_size是1MB，每次读取1MB测试视频流
                        # 如果能获取视频流，则输出读取的时间以及链接
                        if k:
                            print(f'{time.time()-now:.2f}\t{channel_url}')
                            response_time = (time.time()-now) * 1
                            download_speed = 3145728 / response_time / 1024
                            normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                            if response_time > 2:
                                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                                results.append(result)
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

with open("qita.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  广东频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
            if cut_first_chinese_words(channel_name) in guangdong_text:
                if channel_name in channel_counters:
                    if channel_counters[channel_name] >= result_counter:
                        continue
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] += 1
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] = 1
    # 写入其他频道
    channel_counters = {}
    file.write('【  其他频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
            if cut_first_chinese_words(channel_name) not in guangdong_text:
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
print(f"{now_today}其他频道更新完成")

# 合并文件内容
file_contents = []
file_paths = ["cctv.txt", "weishi.txt", "ktpd.txt", "ysyl.txt","xiangang.txt", "qita.txt", "IPV6.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        file_contents.append(content)
        file.close()

# print(f"{now_today}合并文件完成")

# 写入合并后的文件
with open("itvlist.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    output.close()

# print(f"{now_today}写入合并后的文件")
