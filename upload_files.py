import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import random
import time
from datetime import datetime


# 分配文件到不同target，每个target收到的文件不同
def distribute_files(files, num_targets):
    chunk_size = len(files) // num_targets
    distributed = []
    for i in range(num_targets):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_targets - 1 else len(files)
        distributed.append(files[start:end])
    return distributed



# 带重试的上传
def upload_with_retry(src, remote_path, max_retries=3):
    for attempt in range(1, max_retries + 1):
        success = upload_file_to_remote(src, remote_path)
        if success:
            print(f'SUCCESS: 上传 {os.path.basename(src)} 到 {remote_path} (第{attempt}次)')
            return True
        else:
            print(f'FAIL: 上传 {os.path.basename(src)} 到 {remote_path} 失败 (第{attempt}次)')
            time.sleep(0.2)
    print(f'GIVE UP: 上传 {os.path.basename(src)} 到 {remote_path} 最终失败')
    return False

def upload_files_to_remote(file_list, remote_dir):
    for file in file_list:
        src = os.path.join(SOURCE_DIR, file)
        remote_path = os.path.join(remote_dir, file)
        upload_with_retry(src, remote_path)

def main():
    files = os.listdir(SOURCE_DIR)
    distributed = distribute_files(files, len(TARGET_DIRS))
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i, file_list in enumerate(distributed):
            executor.submit(upload_files_to_remote, file_list, TARGET_DIRS[i])

if __name__ == '__main__':
    main()