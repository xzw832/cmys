import ffmpeg

def get_live_source_resolution(url):
    # 使用ffmpeg.input获取输入流
    input_stream = ffmpeg.input(url)
    
    # 使用ffmpeg.output设置输出参数，这里我们不真正输出到文件，而是使用null输出
    # 注意：新版本ffmpeg-python可能不再需要.global_args()
    output_stream = ffmpeg.output(input_stream, 'null', format='null', vframes=1, vf='scale=n:-1')
    
    # 执行FFmpeg命令并获取输出
    ffmpeg_process = output_stream.run()
    ffmpeg_output = ffmpeg_process.stdout.decode()
    
    # 在输出中查找分辨率信息
    for line in ffmpeg_output.split('\n'):
        if 'Stream' in line and 'Video' in line:
            resolution = line.split(',')[0].split(' ')[-1]
            return resolution.split('x')

    return None

# 示例使用
live_source_url = "http://119.54.0.212:9999/hls/48/index.m3u8"  # 替换为你的直播源URL
resolution = get_live_source_resolution(live_source_url)
print(resolution)
