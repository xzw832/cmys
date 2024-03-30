import os
import base64
import requests


# 从环境变量中获取API密钥和基础URL
api_key = "f2c0a15a6c33c43418b37a7027d99b739a38b6bace593b176e0c459a572808b2"
base_url = "https://hunter.qianxin.com/openApi/search"

# 配置信息
spider_cfg = {
    'apiKey': api_key,
    'baseUrl': base_url,
    'search': 'web.body="dbiptv.sn.chinamobile.com" && ip.country=="中国"',
    'page': 1,
    'pageSize': 50,
}

def get_target_list():
    try:
        # 构建API URL
        search_encoded = base64.b64encode(spider_cfg['search'].encode()).decode()
        url = f"{spider_cfg['baseUrl']}?api-key={spider_cfg['apiKey']}&search={search_encoded}&page={spider_cfg['page']}&page_size={spider_cfg['pageSize']}"
        print(url)
        # 发送GET请求
        response = requests.get(url)
        
        # 检查响应状态码
        if response.status_code == 200:
            print(response.text)
            
            # 假设响应的JSON结构与原始Node.js代码中的结构相同
            data = response.json().get('data', {}).get('arr', [])
            return [item['url'] for item in data] if data else []
        else:
            return []
    except Exception as e:
        print(f"获取目标列表时发生错误: {e}")
        return []
item = get_target_list()
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
se=requests.Session()
for lin in item:
    print("--------------------------------->>>>>>>>>>>>>>>>>",lin)
    try:
        res=se.get(lin,headers=headers,timeout=10)
        if res.status_code==200:
            print(res.text)
    except Exception:
        # 无法连接并超时的情况下输出“X”
        print(f'无法连接并超时----------------------->\t{lin}')
