import os
import random
import string
import json
from openpyxl import Workbook

# 配置参数
MIN_WAV_SIZE_MB = 2
MAX_WAV_SIZE_MB = 7
TOTAL_SIZE_LIMIT = 0.01 * 1024 * 1024 * 1024  # 1GB
FILENAME_DIGITS = 18
CONTACT_ID_DIGITS = 5
OUTPUT_XLSX = 'file_names.xlsx'

# 文件输出目录
OUTPUT_DIR = 'output_files'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def random_digits(length):
    return ''.join(random.choices(string.digits, k=length))

def generate_wav_file(filepath, size_mb):
    size_bytes = size_mb * 1024 * 1024
    with open(filepath, 'wb') as f:
        f.write(os.urandom(size_bytes))

def generate_json_file(filepath, contact_id):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({'contact_id': contact_id}, f)

def main():
    total_size = 0
    file_names = []
    while total_size < TOTAL_SIZE_LIMIT:
        # 生成唯一文件名
        filename = random_digits(FILENAME_DIGITS)
        wav_path = os.path.join(OUTPUT_DIR, f'{filename}.wav')
        json_path = os.path.join(OUTPUT_DIR, f'{filename}.json')
        if os.path.exists(wav_path) or os.path.exists(json_path):
            continue  # 避免重名
        # 生成wav文件
        wav_size_mb = random.randint(MIN_WAV_SIZE_MB, MAX_WAV_SIZE_MB)
        generate_wav_file(wav_path, wav_size_mb)
        # 生成json文件
        contact_id = random_digits(CONTACT_ID_DIGITS)
        generate_json_file(json_path, contact_id)
        # 统计大小
        wav_size = os.path.getsize(wav_path)
        json_size = os.path.getsize(json_path)
        total_size += wav_size + json_size
        file_names.append(filename)
        # 超过1G则删除最后一组并退出
        if total_size >= TOTAL_SIZE_LIMIT:
            os.remove(wav_path)
            os.remove(json_path)
            file_names.pop()
            break
    # 写入xlsx
    wb = Workbook()
    ws = wb.active
    ws.title = 'FileNames'
    ws.append(['FileName'])
    for name in file_names:
        ws.append([name])
    wb.save(OUTPUT_XLSX)
    print(f'生成完成，共生成{len(file_names)}组文件，文件名已写入{OUTPUT_XLSX}')

if __name__ == '__main__':
    main()
