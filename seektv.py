import concurrent.futures
import requests
import time

# 自定义请求重试次数
RETRIES = 3

# 自定义请求超时时间（秒）
TIMEOUT = 5

# 自定义User-Agent标识
USER_AGENT = 'okhttp/3.12.11 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'

# 重试逻辑函数
def retry_request(url, session, retries=RETRIES, backoff_factor=0.3, timeout=TIMEOUT):
    for _ in range(retries):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功
            return response.text  # 返回网页文本
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Request to {url} failed: {e}")
            if _ < retries - 1:  # 如果不是最后一次重试，则等待一段时间后重试
                time.sleep(backoff_factor * (2 ** _))  # 指数退避策略
            else:
                print(f"Failed to retrieve URL {url} after {retries} retries")
                return None

# 并发获取网页文本的函数
def concurrent_get_text(urls, max_workers=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 创建requests会话并设置User-Agent
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT

        futures = {executor.submit(retry_request, url, session) for url in urls}
        results = []

        for future in concurrent.futures.as_completed(futures):
            try:
                page_text = future.result()
                if page_text:
                    results.append(page_text)
            except Exception as e:
                print(f"An error occurred while processing a request: {e}")

    return results

# 示例URL列表
urls = [
    "https://raw.githubusercontent.com/taijichadao/tv/main/itvlist.txt",
    "http://api.mcqq.cn/tvbox/zhibo.php",
    "http://tvbox.nx66.bf:99/tvbox/zhibo.php",
    "http://mywlkj.ddns.net:754/tv.php",
    "https://raw.gitcode.com/lionzang/TV/raw/main/channel.txt"
    ]

# 并发获取网页文本
texts = concurrent_get_text(urls, max_workers=10)
all_lines = []
for text in texts:
    lines = text.splitlines()
    all_lines.extend(lines)

# 打印获取到的网页文本
for line in all_lines:
    print('------------------------------------------------------------------------------------------------------------------------')
    print(line)

