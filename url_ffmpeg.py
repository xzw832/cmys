import subprocess
 
def test_stream_resolution(stream_url):
    # 构建ffmpeg命令
    command = ['ffmpeg', '-i', stream_url, '-t', '0.1', '-an', '-vn', '-rw_frame_count', '1', '-loglevel', 'quiet']
    
    # 使用subprocess运行命令
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.decode()}")
        return None
    
    # 解析输出结果获取分辨率
    output_str = output.decode()
    lines = output_str.split('\n')
    for line in lines:
        if 'Video: ' in line:
            parts = line.split(', ')
            for part in parts:
                if 'Video: ' in part:
                    video_info = part.split()
                    if len(video_info) > 2:
                        resolution = video_info[2]
                        return resolution
    return None
 
# 使用示例
stream_url = "http://119.54.0.212:9999/hls/48/index.m3u8"
resolution = test_stream_resolution(stream_url)
if resolution:
    print(f"Stream resolution is: {resolution}")
else:
    print("Unable to determine stream resolution.")
