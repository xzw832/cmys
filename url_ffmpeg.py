import ffmpeg

def get_live_source_resolution(url):
    # 使用ffmpeg.input来获取输入流
    input_stream = ffmpeg.input(url)
    
    # 使用ffmpeg.output来设置输出参数，这里我们不真正输出到文件，而是使用null输出
    output_stream = ffmpeg.output(input_stream, 'null', format='null', vframes=1, vf='scale=n:-1')
    
    # 运行ffmpeg命令并捕获其输出
    ffmpeg_output = output_stream.run_capture()
    
    # 在输出中查找分辨率信息
    for line in ffmpeg_output.stdout.decode().split('\n'):
        if 'Stream' in line and 'Video' in line:
            resolution = line.split(',')[0].split(' ')[-1]
            return resolution.split('x')

    return None

# 示例使用
live_source_url = "http://119.54.0.212:9999/hls/48/index.m3u8"  # 替换为你的直播源URL
resolution = get_live_source_resolution(live_source_url)
print(resolution)
