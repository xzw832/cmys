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
    
all_text = "东莞 中山 佛山 顺德 南海 南方 宝安 岭南 广东 广州 广视 揭西 揭阳 汕头 汕尾 江门 深圳 清远 龙岗 湛江 潮州 珠江 粤语 肇庆 茂名 韶关 云浮 怀化 普宁 珠海 河源 台球 足球 高尔夫 体育 网球 汽车 象棋 围棋 钓鱼 武术 汽摩 爱上 爱体 爱喜 爱奇 爱宠 爱幼 爱怀 爱悬 爱玩 爱生 爱电 爱科 爱经 爱谍 爱赛 爱都 爱院 爱青 牛哥 音乐 江苏 聚鲨 南京 盱眙 沛县 泰州 徐州 淮安 泗洪 东海 宿迁 常州 东海 响水 高淳 新沂 邳州 连云 睢宁 赣榆 水韵 贾汪"
guangdong_text = "东莞 中山 佛山 顺德 南海 南方 宝安 岭南 广东 广州 广视 揭西 揭阳 汕头 汕尾 江门 深圳 清远 龙岗 湛江 潮州 珠江 粤语 肇庆 茂名 韶关 云浮 怀化 普宁 珠海 河源"
tiyu_text = "台球 足球 高尔夫 体育 网球 汽车 象棋 围棋 钓鱼 武术 汽摩 爱上 爱体 爱喜 爱奇 爱宠 爱幼 爱怀 爱悬 爱玩 爱生 爱电 爱科 爱经 爱谍 爱赛 爱都 爱院 爱青 牛哥 音乐"
js_txt="江苏 聚鲨 南京 盱眙 沛县 泰州 徐州 淮安 泗洪 东海 宿迁 常州 东海 响水 高淳 新沂 邳州 连云 睢宁 赣榆 水韵 贾汪"
# 线程安全的队列，用于存储下载任务
task_queue = Queue()
lock = threading.Lock()
qita_channels = []
# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
headers={'User-Agent': 'okhttp/3.12.10(Linux;Android9;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36'}
se=requests.Session()

with open("itv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                name =(f"{channel_name}")
                name = name.replace("高清", "")
                if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
                    if 'CETV' not in channel_name and 'CQTV' not in channel_name and 'IPTV' not in channel_name:
                        if cut_first_chinese_words(channel_name) in all_text:
                            channels.append((name, channel_url))
                        else:
                            qita_channels.append(f"{name},{channel_url}")
    file.close()

# 写入未用的其他频道
qita_channels = set(qita_channels)  # 去重得到唯一的URL列表
qita_channels = sorted(qita_channels)
with open("qita_all.txt", "w", encoding="utf-8") as file:
    for result in qita_channels:
        channel_name, channel_url = result.split(',')
        file.write(f"{channel_name},{channel_url}\n")
    file.close()
    
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
                        if time.time()-now > 20:
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

with open("qita.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  江苏频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
            if 'CETV' not in channel_name and 'CQTV' not in channel_name and 'IPTV' not in channel_name:
                if cut_first_chinese_words(channel_name) in js_txt:
                    if channel_name in channel_counters:
                        if channel_counters[channel_name] >= result_counter:
                            continue
                        else:
                            file.write(f"{channel_name},{channel_url}\n")
                            channel_counters[channel_name] += 1
                    else:
                        file.write(f"{channel_name},{channel_url}\n")
                        channel_counters[channel_name] = 1
                    
    channel_counters = {}
    file.write('【  广东频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
            if 'CETV' not in channel_name and 'CQTV' not in channel_name and 'IPTV' not in channel_name:
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
                    
    channel_counters = {}                
    file.write('【  体育频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' not in channel_name and 'CCTV' not in channel_name and '测试' not in channel_name and '电影' not in channel_name and '影院' not in channel_name and '剧场' not in channel_name and '影视' not in channel_name and '卡通' not in channel_name and '动漫' not in channel_name and '动画' not in channel_name and '少儿' not in channel_name:
            if 'CETV' not in channel_name and 'CQTV' not in channel_name and 'IPTV' not in channel_name:
                if cut_first_chinese_words(channel_name) in tiyu_text:
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
