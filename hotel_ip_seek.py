import random
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
cctv_files = []
weishi_files = []
headers={'User-Agent': 'okhttp/3.12.10(Linux;Android9;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36'}
se=requests.Session()
dcom = [
    "4000",
    "1013",
    "8080",
    "8081",
    "8181",
    "8088",
    "4022",
    "9999",
    "801",
    "9901",
    "8082",
    "18088",
    "808",
    "8001",
    "6666",
    "8083",
    "8084",
    "8888",
    "8090",
    "8008"
    
]
js_txt="江苏 聚鲨 南京 盱眙 沛县 泰州 徐州 淮安 泗洪 东海 宿迁 常州 东海 响水 高淳 新沂 邳州 连云 睢宁 赣榆 水韵 贾汪"
urls = []
# 更新文件数据
def replace_line_in_file(file_path, target_string, new_line):
    # 读取文件内容到列表中，每行是一个元素
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 遍历每一行，如果找到目标字符串，就替换整行
    for i, line in enumerate(lines):
        if target_string in line:
            lines[i] = new_line + '\n'  # 确保新行以换行符结尾
    file.close()

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    file.close()

# 初始化计数器为0
counter = 0
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter
    
# 返回IP地址+端口
def ret_urls(url):
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find("/", ip_start_index)  # 查找下一个"/"的位置，用来确定IP地址的结束位置
    
    # 提取IP地址
    if ip_end_index != -1:
        ip_address = url[ip_start_index:ip_end_index]
    else:
        # 如果没有找到下一个"/"，则假设URL的末尾就是IP地址的结束位置
        ip_address = url[ip_start_index:]
    return ip_address

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
with open("cfg_ip.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if 'http' in channel_url:
                    urls.append(f"{channel_name},{channel_url}")
                else:
                    if '有效' in channel_name:
                        break
    file.close()
ip_list = []
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
    if ip_address not in ip_list:
        ip_list.append((ip_address))
        for i in range(1, 255):
            modified_ip = f"{ip_address[:-1]}{i}"
            modified_url = f"{ip_start}{modified_ip}:{port}{ip_end}"
            # print(modified_url)
            channels.append((channel, modified_url))
           

def is_url_accessible(url):
    try:
        return url
    except requests.exceptions.RequestException:
        pass
    # return None
    return url

valid_urls = []
#   多线程获取可用url
for ipv in urls:
    url = ipv.strip()
    if "http" in url:
        modify_urls(url)
        
channels = set(channels)

# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        # print(channel_name, channel_url)
        if "m3u8" in channel_url or "flv" in channel_url:
            try:
                print(channel_name, channel_url)
                channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
                lines = requests.get(channel_url,headers=headers, timeout=3, stream=True).text.strip().split('\n')  # 获取m3u8文件内容
                ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
                ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
                ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接
    
                # 多获取的视频数据进行5秒钟限制
                with eventlet.Timeout(10, False):
                    start_time = time.time()
                    content = requests.get(ts_url,headers=headers, timeout=(4,5), stream=True).content
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
                print(f'X Error \t{channel_name},{channel_url}')
                # 获取锁
                lock.acquire()
                error_channels.append(error_channel)
                # 释放锁
                lock.release()
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
        else:
            try:
                now=time.time()
                chunk_size = 5242880
                res=se.get(channel_url,headers=headers,stream=True,timeout=5)
                if res.status_code==200:
                    total_received = 0
                    for k in res.iter_content(chunk_size=chunk_size):
                        # 这里的chunk_size是1MB，每次读取1MB测试视频流
                        # 如果能获取视频流，则输出读取的时间以及链接
                        if time.time()-now > 35:
                            res.close()
                            print(f'Time out\t{channel_url}')
                            break
                        else:
                            if k:
                                chunk_len = len(k)
                                if chunk_len >= chunk_size:
                                    print(f'{time.time()-now:.2f}\t{channel_url}')
                                    response_time = (time.time()-now) * 1
                                    download_speed = chunk_len / response_time / 1024
                                    normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                                    if response_time > 2.8:
                                        result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                                        # 获取锁
                                        lock.acquire()
                                        results.append(result)
                                        # 释放锁
                                        lock.release()
                                    else:
                                        print(f'X\t{channel_url}')
                                    break
                                else:
                                    print(f'X 数据块小于设置值 \t{channel_url}')
            except:
                # 无法连接并超时的情况下输出“X”
                print(f'X\t{channel_url}')
        
        # 减少CPU占用
        time.sleep(random.randint(3, 10))
        # 标记任务完成
        task_queue.task_done()

# 创建多个工作线程
num_threads = 100
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True) 
    #t = threading.Thread(target=worker, args=(event,len(channels)))  # 将工作线程设置为守护线程
    t.start()
    #event.set()

# 添加下载任务到队列
for channel in channels:
    # print(channel)
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()

# 如果存在于检测列表时，表示已失效，清空原来的源
cctv_00 = 0
cctv_11 = 0
cctv_12 = 0
cctv_13 = 0
cctv_14 = 0
cctv_15 = 0
cctv_20 = 0
cctv_21 = 0
cctv_22 = 0
cctv_23 = 0
for url in urls:
    channel_name, channel_url = url.split(',')
    if '11_央卫秒开' in channel_name:
        cctv_11 = 1
    elif '0_央卫秒开' in channel_name:
        cctv_00 = 1
    elif '12_央卫秒开' in channel_name:
        cctv_12 = 1
    elif '13_央卫秒开' in channel_name:
        cctv_13 = 1
    elif '14_央卫秒开' in channel_name:
        cctv_14 = 1
    elif '15_央卫秒开' in channel_name:
        cctv_15 = 1
    elif '20_央卫秒开' in channel_name:
        cctv_20 = 1
    elif '21_央卫秒开' in channel_name:
        cctv_21 = 1
    elif '22_央卫秒开' in channel_name:
        cctv_22 = 1
    elif '23_央卫秒开' in channel_name:
        cctv_23 = 1        
        
if cctv_00 == 1:
    with open('Z_00_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_00_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
if cctv_11 == 1:
    with open('Z_11_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_11_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
if cctv_12 == 1:
    with open('Z_12_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_12_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
if cctv_13 == 1:
    with open('Z_13_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_13_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()    
if cctv_14 == 1:
    with open('Z_14_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_14_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()   
if cctv_15 == 1:
    with open('Z_15_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_15_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
if cctv_20 == 1:
    with open('Z_20_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_20_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()  
if cctv_21 == 1:
    with open('Z_21_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_21_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
if cctv_22 == 1:
    with open('Z_22_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_22_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()    
if cctv_23 == 1:
    with open('Z_23_cctv.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
    with open('Z_23_weishi.txt', 'w', encoding='utf-8') as file:
        pass
    file.close()
results = sorted(results, reverse=True)

for result in results:
    channel_name, channel_url, speed = result
    print(result)
    if '11_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("11_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('11_央卫秒开', url)
            cctv_files.append(filedata)

            with open("11_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('11_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_11_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_11_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()

    elif '12_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("12_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('12_央卫秒开', url)
            cctv_files.append(filedata)

            with open("12_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('12_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_12_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_12_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()
    elif '13_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("13_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('13_央卫秒开', url)
            cctv_files.append(filedata)

            with open("13_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('13_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_13_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_13_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()  
    elif '14_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("14_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('14_央卫秒开', url)
            cctv_files.append(filedata)

            with open("14_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('14_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_14_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_15_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()     
    elif '15_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("15_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('15_央卫秒开', url)
            cctv_files.append(filedata)

            with open("15_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('15_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_15_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_15_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()                     
    elif '0_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("prv_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('0_央卫秒开', url)
            cctv_files.append(filedata)

            with open("prv_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('0_央卫秒开', url)
            weishi_files.append(weishi_filedata)
            # 保存，
            with open("Z_00_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_00_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()
    elif '20_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("20_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('20_央卫秒开', url)
            cctv_files.append(filedata)

            with open("20_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('20_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_20_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_20_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()    
    elif '21_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("21_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('21_央卫秒开', url)
            cctv_files.append(filedata)

            with open("21_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('21_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_21_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_21_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close() 
    elif '22_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("22_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('22_央卫秒开', url)
            cctv_files.append(filedata)

            with open("22_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('22_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_22_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_22_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()    
    elif '23_央卫秒开' in channel_name:
        url = ret_urls(channel_url)
        print(url)
        if len(url) > 0:
            increment_counter()
            cctv_files = []
            weishi_files = []
            with open("23_cctv.txt", 'r', encoding='utf-8') as file:
                filedata = file.read()
            file.close()
            filedata = filedata.replace('23_央卫秒开', url)
            cctv_files.append(filedata)

            with open("23_weishi.txt", 'r', encoding='utf-8') as file:
                weishi_filedata = file.read()
            file.close()
            weishi_filedata = weishi_filedata.replace('23_央卫秒开', url)
            weishi_files.append(weishi_filedata)

            # 保存，
            with open("Z_23_cctv.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(cctv_files))
                output.close()
            with open("Z_23_weishi.txt", "w", encoding="utf-8") as output:
                output.write('\n'.join(weishi_files))
                output.close()    
# 合并文件内容
file_contents = []
file_paths = ["Z_22_cctv.txt", "Z_21_cctv.txt", "Z_20_cctv.txt", "Z_15_cctv.txt", "Z_14_cctv.txt", "Z_13_cctv.txt", "Z_12_cctv.txt", "Z_11_cctv.txt", "Z_00_cctv.txt", "Z_23_cctv.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
            file.close()
# 写入合并后的文件
with open("S_CCTV.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    output.close()

# print("================================================================================================================")
# 合并文件内容
file_contents = []
file_paths = ["Z_22_weishi.txt", "Z_21_weishi.txt", "Z_20_weishi.txt", "Z_15_weishi.txt", "Z_14_weishi.txt", "Z_13_weishi.txt", "Z_12_weishi.txt", "Z_11_weishi.txt", "Z_00_weishi.txt", "Z_23_weishi.txt", "S_CCTV.txt"]  # 替换为实际的文件路径列表
for file_path in file_paths:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            file_contents.append(content)
            file.close()
# 写入合并后的文件
with open("S_weishi.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    output.close()

file_path = "cfg_ip.txt"
# 将结果写入文件
with open("seekip_ok.txt", 'w', encoding='utf-8') as out_file:
    for result in results:
        channel_name, channel_url, speed = result
        out_file.write(f"{channel_name},{channel_url}\n")
        new_line = f"{channel_name},{channel_url}"
        replace_line_in_file(file_path, channel_name, new_line)
        time.sleep(1)
    out_file.write(f"测试完成时间,{now_today}\n")
    out_file.close()


# 使用示例

print(f"{now_today}ip测试完成")
