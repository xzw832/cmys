import concurrent.futures
import requests
import time
import threading

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

# 去除重复项
unique_urls = list(set(all_lines))

# 去除空格
cleaned_urls = [url.strip() for url in all_lines]
# 打印获取到的网页文本

# 定义执行GET请求的函数
def get_with_retries(url, user_agent, timeout=10, retries=3):
    headers = {'User-Agent': user_agent}
    session = requests.Session()
    line = url.strip()
    count = line.count(',')
    if count == 1:
        if line:
            channel_name, channel_url = line.split(',')
            if "http" in channel_url and "[" not in channel_url:
                for _ in range(retries):
                    try:
                        response = session.get(channel_url, allow_redirects=True, headers=headers, timeout=timeout)
                        response.raise_for_status()  # 如果HTTP请求返回了不成功的状态码，将引发HTTPError异常
                        next_url = response.url
                        new_url = f"{channel_name},{next_url}"
                        return new_url  # 返回重定向后的URL
                    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                        print(f"Error occurred for URL {channel_url}: {e}")
                        if retries > 1:  # 如果还有重试次数，则等待后重试
                            time.sleep(1)  # 等待1秒后再重试
                        else:
                            print(f"No more retries for URL {channel_url}")
                            return url  # 没有更多重试，返回None
    
    session.close()  # 关闭session
    return url

# 主函数，用于并发执行GET请求
def concurrent_get_with_retries(urls, user_agent, max_workers, timeout=10, retries=3):
    threads = []
    results = []

    # 创建线程池
    for url in urls:
        thread = threading.Thread(target=get_with_retries, args=(url, user_agent, timeout, retries))
        thread.start()
        threads.append(thread)

        # 当线程数量达到最大工作线程数时，等待一个线程完成
        if len(threads) >= max_workers:
            for thread in threads:
                thread.join()
            threads = []

    # 等待所有剩余的线程完成
    for thread in threads:
        thread.join()

    return results

# 设置URL列表和User-Agent
user_agent = "okhttp/3.12.11 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
max_workers = 5  # 设置线程数量

# 调用并发函数并打印结果
results = concurrent_get_with_retries(cleaned_urls, user_agent, max_workers)
for url, redirected_url in zip(cleaned_urls, results):
    print(f"Original URL: {url}, Redirected URL: {redirected_url} if any")
