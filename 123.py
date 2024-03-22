import requests

channel_url = 'http://mywlkj.ddns.net:754/tv/1905.php?id=cctv6'  # 替换为你想测试的URL
response = requests.get(channel_url, allow_redirects=True)

# 检查是否有重定向发生
if response.history:
    # 如果有重定向历史，说明发生了重定向
    print("发生了重定向")
    # 获取最终重定向到的地址
    final_url = response.url
    print("最终地址:", final_url)
else:
    # 如果没有重定向历史，说明没有发生重定向
    print("没有发生重定向")
    # 返回原始请求的地址
    original_url = url
    print("原始地址:", original_url)
