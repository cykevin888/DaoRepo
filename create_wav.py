import wave
import struct
import math
import random
import json
import os
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from uuid import uuid4

def generate_wav(filename, size_mb, duration=None):
    framerate = 44100
    sampwidth = 2
    nchannels = 1
    amplitude = 32767
    frequency = random.randint(200, 1000)
    # 计算需要的帧数
    nframes = int((size_mb * 1024 * 1024) / (framerate * sampwidth * nchannels) * framerate)
    if duration:
        nframes = int(duration * framerate)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        for i in range(nframes):
            value = int(amplitude * math.sin(2 * math.pi * frequency * i / framerate))
            data = struct.pack('<h', value)
            wf.writeframesraw(data)

def generate_json(filename, wav_filename):
    contact_id = str(random.randint(10 ** 7, 10 ** 8 - 1))  # 8位随机数字
    data = {
        "audio_file": wav_filename,
        "label": random.choice(["cat", "dog", "bird", "music", "noise"]),
        "duration": random.uniform(5, 120),
        "contact_id": contact_id,
        "meta": {
            "created": datetime.now().isoformat(),
            "desc": "mock data"
        }
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            total += os.path.getsize(fp)
    return total

def generate_one_sample(args):
    output_dir, max_total_bytes = args
    name = datetime.now().strftime("%Y%m%d%H%M%S%f") + uuid4().hex[:6]
    wav_path = os.path.join(output_dir, f"{name}.wav")
    json_path = os.path.join(output_dir, f"{name}.json")
    size_mb = random.randint(5, 20)
    generate_wav(wav_path, size_mb)
    generate_json(json_path, f"{name}.wav")
    total_size = get_dir_size(output_dir)
    print(f"生成: {wav_path} ({size_mb}MB), {json_path}，累计大小：{total_size/1024/1024/1024:.2f}GB")
    if total_size >= max_total_bytes:
        print(f"总大小已超过{max_total_bytes/1024/1024/1024:.2f}GB，停止生成。")
        return False
    return True

def generate_mock_data(n, output_dir="mock_data", max_total_gb=100, max_workers=4):
    os.makedirs(output_dir, exist_ok=True)
    max_total_bytes = max_total_gb * 1024 * 1024 * 1024
    futures = []
    args_list = [(output_dir, max_total_bytes) for _ in range(n)]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for args in args_list:
            futures.append(executor.submit(generate_one_sample, args))
        for future in as_completed(futures):
            # 如果有一个返回False，说明空间超限，后续可考虑取消任务
            if not future.result():
                break

if __name__ == "__main__":
    generate_mock_data(n=5, max_total_gb=0.05, max_workers=4)  # n设大一点，max_total_gb=100