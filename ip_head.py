import requests

def get_redirected_urls(url_list):
    redirected_urls = []
    for line in url_list:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if 'http' in channel_url:
                    session = requests.Session()
                    response = requests.head(channel_url, allow_redirects=True)
                    if response.status_code == 200 and 'Location' in response.headers:
                        redirected_url = response.headers['Location']
                        redirected_response = session.head(redirected_url)
                        new_url = channel_name, redirected_response.url
                        redirected_urls.append(new_url)
                    elif response.status_code in [301, 302, 303, 307, 308]:
                        new_url = channel_name, response.headers['Location']
                        redirected_urls.append(new_url)
                    else:
                        new_url = channel_name, channel_url
                        redirected_urls.append(new_url)
            else:
                redirected_urls.append(line)
        else:
            redirected_urls.append(line)
            
    return redirected_urls

# 示例用法
url_list = [
    "HBO_HD,http://mywlkj.ddns.net:754/tv/haiou.php?id=1",
    "HBO_HITS,http://mywlkj.ddns.net:754/tv/haiou.php?id=2",
    "HBOSignatureHD,http://mywlkj.ddns.net:754/tv/haiou.php?id=3",
    "HBO温馨家庭,http://mywlkj.ddns.net:754/tv/haiou.php?id=4",
    "华纳电影台,http://mywlkj.ddns.net:754/tv/haiou.php?id=5",
    "惊辣Thrill,http://mywlkj.ddns.net:754/tv/haiou.php?id=6",
    "8度空间HD,http://mywlkj.ddns.net:754/tv/haiou.php?id=7",
    "欢喜台HD,http://mywlkj.ddns.net:754/tv/haiou.php?id=8",
    "全佳台HD,http://mywlkj.ddns.net:754/tv/haiou.php?id=9",
    "爱奇艺HD,http://mywlkj.ddns.net:754/tv/haiou.php?id=10",
    "凤凰香港台,http://mywlkj.ddns.net:754/tv/haiou.php?id=11",
    "凤凰中文台,http://mywlkj.ddns.net:754/tv/haiou.php?id=12",
    "凤凰资讯台,http://mywlkj.ddns.net:754/tv/haiou.php?id=13",
    "TVB翡翠台,http://mywlkj.ddns.net:754/tv/haiou.php?id=14",
    "TVBJ2台,http://mywlkj.ddns.net:754/tv/haiou.php?id=15",
    "TVB明珠台,http://mywlkj.ddns.net:754/tv/haiou.php?id=16",
    "TVB华丽翡翠台,http://mywlkj.ddns.net:754/tv/haiou.php?id=17",
    "TVB星河台(粤),http://mywlkj.ddns.net:754/tv/haiou.php?id=18",
    "TVB星河台(国),http://mywlkj.ddns.net:754/tv/haiou.php?id=19",
    "TVB星河台(粤),http://mywlkj.ddns.net:754/tv/haiou.php?id=20",
    "港台RHK31,http://mywlkj.ddns.net:754/tv/haiou.php?id=21",
    "港台RHK32,http://mywlkj.ddns.net:754/tv/haiou.php?id=22",
    "VIU TV,http://mywlkj.ddns.net:754/tv/haiou.php?id=23",
    "VIU TV6,http://mywlkj.ddns.net:754/tv/haiou.php?id=24",
    "TVB无线新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=25",
    "TVB财经体育资讯2台,http://mywlkj.ddns.net:754/tv/haiou.php?id=26",
    "美亚电影台,http://mywlkj.ddns.net:754/tv/haiou.php?id=27",
    "天映经典,http://mywlkj.ddns.net:754/tv/haiou.php?id=28",
    "天映频道,http://mywlkj.ddns.net:754/tv/haiou.php?id=29",
    "CINEMAX,http://mywlkj.ddns.net:754/tv/haiou.php?id=30",
    "AXN,http://mywlkj.ddns.net:754/tv/haiou.php?id=31",
    "tvNMovie,http://mywlkj.ddns.net:754/tv/haiou.php?id=32",
    "民视,http://mywlkj.ddns.net:754/tv/haiou.php?id=33",
    "台视,http://mywlkj.ddns.net:754/tv/haiou.php?id=34",
    "中视,http://mywlkj.ddns.net:754/tv/haiou.php?id=35",
    "华视,http://mywlkj.ddns.net:754/tv/haiou.php?id=36",
    "公视,http://mywlkj.ddns.net:754/tv/haiou.php?id=37",
    "TVBS,http://mywlkj.ddns.net:754/tv/haiou.php?id=38",
    "台视综合台,http://mywlkj.ddns.net:754/tv/haiou.php?id=39",
    "民视台湾台,http://mywlkj.ddns.net:754/tv/haiou.php?id=40",
    "三立综合台,http://mywlkj.ddns.net:754/tv/haiou.php?id=41",
    "三立台湾台,http://mywlkj.ddns.net:754/tv/haiou.php?id=42",
    "三立戏剧台,http://mywlkj.ddns.net:754/tv/haiou.php?id=43",
    "三立都会台,http://mywlkj.ddns.net:754/tv/haiou.php?id=44",
    "八大综合台,http://mywlkj.ddns.net:754/tv/haiou.php?id=45",
    "八大第一台,http://mywlkj.ddns.net:754/tv/haiou.php?id=46",
    "八大戏剧台,http://mywlkj.ddns.net:754/tv/haiou.php?id=47",
    "爱尔达综合,http://mywlkj.ddns.net:754/tv/haiou.php?id=48",
    "爱尔达影剧,http://mywlkj.ddns.net:754/tv/haiou.php?id=49",
    "中天亚洲台,http://mywlkj.ddns.net:754/tv/haiou.php?id=50",
    "中天综合台,http://mywlkj.ddns.net:754/tv/haiou.php?id=51",
    "中天娱乐台,http://mywlkj.ddns.net:754/tv/haiou.php?id=52",
    "TVBS欢乐台,http://mywlkj.ddns.net:754/tv/haiou.php?id=53",
    "龙详时代台,http://mywlkj.ddns.net:754/tv/haiou.php?id=54",
    "东森电影台,http://mywlkj.ddns.net:754/tv/haiou.php?id=55",
    "东森洋片台,http://mywlkj.ddns.net:754/tv/haiou.php?id=56",
    "东森综合台,http://mywlkj.ddns.net:754/tv/haiou.php?id=57",
    "东森戏剧台,http://mywlkj.ddns.net:754/tv/haiou.php?id=58",
    "东森超视台,http://mywlkj.ddns.net:754/tv/haiou.php?id=59",
    "好莱坞电影台,http://mywlkj.ddns.net:754/tv/haiou.php?id=60",
    "緯來電影台,http://mywlkj.ddns.net:754/tv/haiou.php?id=61",
    "卫视洋片台,http://mywlkj.ddns.net:754/tv/haiou.php?id=62",
    "龙华戏剧台,http://mywlkj.ddns.net:754/tv/haiou.php?id=63",
    "龙华偶像台,http://mywlkj.ddns.net:754/tv/haiou.php?id=64",
    "龙华洋片台,http://mywlkj.ddns.net:754/tv/haiou.php?id=65",
    "龙华电影台,http://mywlkj.ddns.net:754/tv/haiou.php?id=66",
    "TVBS新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=67",
    "中天新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=68",
    "台视新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=69",
    "中视新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=70",
    "民视新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=71",
    "东森新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=72",
    "东森财经台,http://mywlkj.ddns.net:754/tv/haiou.php?id=73",
    "寰宇新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=74",
    "非凡新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=75",
    "年代新闻台,http://mywlkj.ddns.net:754/tv/haiou.php?id=76",
    "WWEHD,http://mywlkj.ddns.net:754/tv/haiou.php?id=77",
    "爱尔达体育2台,http://mywlkj.ddns.net:754/tv/haiou.php?id=78",
    "博斯运动1,http://mywlkj.ddns.net:754/tv/haiou.php?id=79",
    "博斯运动2,http://mywlkj.ddns.net:754/tv/haiou.php?id=80",
    "博斯高球台,http://mywlkj.ddns.net:754/tv/haiou.php?id=81",
    "博斯网球台,http://mywlkj.ddns.net:754/tv/haiou.php?id=82",
    "Supersports1,http://mywlkj.ddns.net:754/tv/haiou.php?id=83",
    "Supersports4,http://mywlkj.ddns.net:754/tv/haiou.php?id=84",
    "SonyTen1,http://mywlkj.ddns.net:754/tv/haiou.php?id=85",
    "SonyTen2,http://mywlkj.ddns.net:754/tv/haiou.php?id=86",
    "SonyTen3,http://mywlkj.ddns.net:754/tv/haiou.php?id=87",
    "纬来体育台,http://mywlkj.ddns.net:754/tv/haiou.php?id=88",
    "纬来日本台,http://mywlkj.ddns.net:754/tv/haiou.php?id=89",
    "EYETV旅游,http://mywlkj.ddns.net:754/tv/haiou.php?id=90",
    "EYETV戏剧,http://mywlkj.ddns.net:754/tv/haiou.php?id=91",
    "Momo综合,http://mywlkj.ddns.net:754/tv/haiou.php?id=92",
    "靖天国际台,http://mywlkj.ddns.net:754/tv/haiou.php?id=93",
    "靖天卡通台,http://mywlkj.ddns.net:754/tv/haiou.php?id=94",
    "大爱电视台,http://mywlkj.ddns.net:754/tv/haiou.php?id=95",
    "美食星球台,http://mywlkj.ddns.net:754/tv/haiou.php?id=96",
    "亚洲旅游台,http://mywlkj.ddns.net:754/tv/haiou.php?id=97",
    "TLC旅游台,http://mywlkj.ddns.net:754/tv/haiou.php?id=98",
    "国家地理野生,http://mywlkj.ddns.net:754/tv/haiou.php?id=99",
    "国家地理台湾,http://mywlkj.ddns.net:754/tv/haiou.php?id=100",
    "DiscoveryAsia,http://mywlkj.ddns.net:754/tv/haiou.php?id=101",
    "DiscoveryHD,http://mywlkj.ddns.net:754/tv/haiou.php?id=102",
]

redirected_urls = get_redirected_urls(url_list)

for line in redirected_urls:
    print(line)
