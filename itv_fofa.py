import requests
 
API_URL = "https://fofa.info/api/v1/search/all"
API_KEY = "g832@qq.com"
SECRET = "01eb0c0d94dab0f234627012f7e6b527"
QUERY = "你的查询语句"  # 例如: "protocol=\"http\""
 
PAGE = 1
PAGE_SIZE = 50  # 每页条数，fofa API 限制最大 100
 
def get_token(key, secret):
    url = "https://fofa.info/api/v1/info/ip"
    data = {
        "email": key,
        "key": secret
    }
    response = requests.post(url, data=data)
    return response.json()["data"]["Token"]
 
def search_fofa(query, page, page_size, token):
    url = API_URL
    data = {
        "email": API_KEY,
        "key": SECRET,
        "qbase64": base64.b64encode(query.encode('utf-8')).decode('utf-8'),
        "page": page,
        "size": page_size,
        "token": token
    }
    headers = {
        "Range": f"items {page}-{page_size}"
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()
 
if __name__ == "__main__":
    token = get_token(API_KEY, SECRET)
    results = search_fofa(QUERY, PAGE, PAGE_SIZE, token)
    # 处理结果
    for result in results:
        print(result)
