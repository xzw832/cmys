import os
import re
import time
import requests
from requests.exceptions import Timeout
import chardet

now_today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
load_urls = [
    "http://tvbox.nx66.bf:99/tvbox/zhibo.php",
    "http://api.mcqq.cn/tvbox/zhibo.php",
    "http://39.101.135.137:8081/ls.txt",
    "https://raw.gitcode.com/lionzang/TV/raw/main/channel.txt",
    "https://gitee.com/chuangxin-chuang_0/cysmlzx/raw/master/iptv.txt",
    "http://107.174.127.132:2082/getplaylist?user=tianya666&type=txt"
    ]
file_contents = []
results = []
for url in load_urls:
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        if response.status_code == 200:
            file_contents.append(f"//地址：{url}\n")
            # print(response.text)
            detected_encoding = chardet.detect(response.content)['encoding']
            if detected_encoding is not None:
                content = response.content.decode(detected_encoding, errors='ignore')
            else:
                # 你可以选择一个默认的编码，或者记录一个错误，或者采取其他措施
                content = response.content.decode('utf-8', errors='ignore')
            file_contents.append(content)
    except:
        print(f"=============Errot============={url}")
url_list = [line for line_str in file_contents for line in line_str.split('\n')]
def text_name(put_name):
    name =(f"{put_name}")
    name = name.replace("cctv", "CCTV")
    name = name.replace("中央", "CCTV")
    name = name.replace("央视", "CCTV")
    name = name.replace("高清", "")
    name = name.replace("超高", "")
    name = name.replace("HD", "")
    name = name.replace("标清", "")
    name = name.replace("频道", "")
    name = name.replace("-", "")
    name = name.replace("·", "")
    name = name.replace(" ", "")
    name = name.replace("PLUS", "+")
    name = name.replace("＋", "+")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
    name = name.replace("CCTV1综合", "CCTV1")
    name = name.replace("CCTV2财经", "CCTV2")
    name = name.replace("CCTV3综艺", "CCTV3")
    name = name.replace("CCTV4国际", "CCTV4")
    name = name.replace("CCTV4中文国际", "CCTV4")
    name = name.replace("CCTV4欧洲", "CCTV4")
    name = name.replace("CCTV5体育", "CCTV5")
    name = name.replace("CCTV6电影", "CCTV6")
    name = name.replace("CCTV7军事", "CCTV7")
    name = name.replace("CCTV7军农", "CCTV7")
    name = name.replace("CCTV7农业", "CCTV7")
    name = name.replace("CCTV7国防军事", "CCTV7")
    name = name.replace("CCTV8电视剧", "CCTV8")
    name = name.replace("CCTV9记录", "CCTV9")
    name = name.replace("CCTV9纪录", "CCTV9")
    name = name.replace("CCTV10科教", "CCTV10")
    name = name.replace("CCTV11戏曲", "CCTV11")
    name = name.replace("CCTV12社会与法", "CCTV12")
    name = name.replace("CCTV13新闻", "CCTV13")
    name = name.replace("CCTV新闻", "CCTV13")
    name = name.replace("CCTV14少儿", "CCTV14")
    name = name.replace("CCTV15音乐", "CCTV15")
    name = name.replace("CCTV16奥林匹克", "CCTV16")
    name = name.replace("CCTV17农业农村", "CCTV17")
    name = name.replace("CCTV17农业", "CCTV17")
    name = name.replace("CCTV5+体育赛视", "CCTV5+")
    name = name.replace("CCTV5+体育赛事", "CCTV5+")
    name = name.replace("CCTV5+体育", "CCTV5+")
    name = name.replace("CMIPTV", "")
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
    return name
    
def text_list(list_str):
    if len(list_str) > 0:
        if '#genre#' in list_str:
            results.append(list_str)
        elif '#' in list_str:
            part_before_comma = list_str.split(',')[0]
            part_before_comma = text_name(part_before_comma)
            parts = list(filter(None, list_str.split("#")))
            for line in parts:
                print(line)
                count = line.count(',')
                if count == 0:
                    results.append(f"{part_before_comma},{line.strip()}")
                else:
                    count = line.count(',')
                    if count == 1:
                        channel_name, channel_url = line.strip().split(',')
                        name = text_name(channel_name)
                        results.append(f"{name},{channel_url}")
                    else:
                        results.append(line.strip())
        else:
            count = list_str.count(',')
            if count == 1:
                channel_name, channel_url = list_str.strip().split(',')
                name = text_name(channel_name)
                results.append(f"{name},{channel_url}")
            else:
                results.append(list_str.strip())
    
for result in url_list:
    text_list(result)
    # print(result)

# 将结果写入文件
with open("nanxun_tv.txt", 'w', encoding='utf-8') as file:
    for result in results:
        # print(result)
        file.write(f"{result}\n")
    file.write(f"更新时间：{now_today}\n")
    file.close()

results_list = set(results)
results_set = sorted(results_list)
# 分离出移动源
with open("chinamobile.txt", 'w', encoding='utf-8') as file:
    for result in results_set:
        if 'http://ottrrs.hl.chinamobile.com' in result or '/dbiptv.sn.chinamobile.com/' in result:
            if '://[' not in result:
                line = result.strip()
                count = line.count(',')
                if count == 1:
                    if line:
                        channel_name, channel_url = line.split(',')
                        name =(f"{channel_name}")
                        file.write(f"{name}_移动,{channel_url}\n")
                        print(f"{name},{channel_url}")
    file.write(f"更新时间：{now_today}\n")
    file.close()
