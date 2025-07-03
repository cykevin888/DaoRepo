import wave
import struct
import math
import random
import json
import os
from datetime import datetime, timedelta

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
    data = {
        "audio_file": wav_filename,
        "label": random.choice(["cat", "dog", "bird", "music", "noise"]),
        "duration": random.uniform(5, 120),
        "meta": {
            "created": datetime.now().isoformat(),
            "desc": "mock data"
        }
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_mock_data(n, output_dir="mock_data"):
    os.makedirs(output_dir, exist_ok=True)
    used_names = set()
    base_time = datetime.now()
    for i in range(n):
        # 生成唯一14位数字（年月日时分秒+微秒后两位）
        while True:
            dt = base_time + timedelta(seconds=i)
            name = dt.strftime("%Y%m%d%H%M%S")
            # 保证唯一
            if name not in used_names:
                used_names.add(name)
                break
        wav_path = os.path.join(output_dir, f"{name}.wav")
        json_path = os.path.join(output_dir, f"{name}.json")
        size_mb = random.randint(5, 20)
        generate_wav(wav_path, size_mb)
        generate_json(json_path, f"{name}.wav")
        print(f"生成: {wav_path} ({size_mb}MB), {json_path}")

if __name__ == "__main__":
    generate_mock_data(n=5)  # 生成5组，可自行修改