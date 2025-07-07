import os
import json
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from batch_planner import get_batch_info, get_next_batch
import datetime

MAX_ZIP_SIZE = 2 * 1024 * 1024 * 1024  # 2G
MAX_ZIP_COUNT = 10
SOURCE_FOLDER = 'source_folder'
NEXT_BATCH_FOLDER = 'next_batch_source_folder'

def group_files(source_folder):
    """
    遍历source_folder，配对同名json和wav文件，返回[(json_path, wav_path), ...]
    """
    files = os.listdir(source_folder)
    json_files = {os.path.splitext(f)[0]: os.path.join(source_folder, f) for f in files if f.endswith('.json')}
    wav_files = {os.path.splitext(f)[0]: os.path.join(source_folder, f) for f in files if f.endswith('.wav')}
    groups = []
    for name in json_files:
        if name in wav_files:
            groups.append((json_files[name], wav_files[name]))
    return groups

def split_batches(file_groups, max_zip_size, max_zip_count):
    """
    按zip最大体积分组，返回batches, extra_files
    batches: [[(json, wav), ...], ...]
    extra_files: [(json, wav), ...]
    """
    batches = []
    current_batch = []
    current_size = 0
    for group in file_groups:
        size = os.path.getsize(group[0]) + os.path.getsize(group[1])
        if current_size + size > max_zip_size and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_size = 0
        current_batch.append(group)
        current_size += size
    if current_batch:
        batches.append(current_batch)
    # 超出最大zip数的文件组
    if len(batches) > max_zip_count:
        extra_batches = batches[max_zip_count:]
        batches = batches[:max_zip_count]
        extra_files = [item for batch in extra_batches for item in batch]
    else:
        extra_files = []
    return batches, extra_files

def zip_files(batch_id, zip_num, file_group, output_folder):
    """
    打包成zip，返回zip文件路径
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    zip_name = f"{batch_id}_{zip_num:02d}.zip"
    zip_path = os.path.join(output_folder, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for json_path, wav_path in file_group:
            zipf.write(json_path, arcname=os.path.basename(json_path))
            zipf.write(wav_path, arcname=os.path.basename(wav_path))
    return zip_path

def producer_task(batch_id, zip_num, file_group, output_folder, queue):
    zip_path = zip_files(batch_id, zip_num, file_group, output_folder)
    queue.put(zip_path)

def move_extra_files(extra_files, next_batch_folder):
    if not os.path.exists(next_batch_folder):
        os.makedirs(next_batch_folder)
    for json_path, wav_path in extra_files:
        shutil.move(json_path, os.path.join(next_batch_folder, os.path.basename(json_path)))
        shutil.move(wav_path, os.path.join(next_batch_folder, os.path.basename(wav_path)))

def get_batch_id():
    from datetime import datetime
    now = datetime.now()
    return now.strftime('%Y%m%d')

def main():
    n_batches = 24  # 可根据需要调整
    now = datetime.datetime.now()
    date, batch_no, batch_id = get_batch_info(n_batches, now)
    next_date, next_batch_no, next_batch_id = get_next_batch(date, batch_no, n_batches)
    output_folder = f"output_{batch_id}"
    NEXT_BATCH_FOLDER = f"source_{next_batch_id}"
    CUR_BATCH_FOLDER = f"source_{batch_id}"

    # 1. 优先处理上次遗留
    file_groups = []
    if os.path.exists(CUR_BATCH_FOLDER):
        file_groups += group_files(CUR_BATCH_FOLDER)
    file_groups += group_files(SOURCE_FOLDER)

    # 2. 分批打包
    batches, extra_files = split_batches(file_groups, MAX_ZIP_SIZE, MAX_ZIP_COUNT)
    # 3. 线程池生产者
    queue = Queue()
    with ThreadPoolExecutor(max_workers=2) as executor:
        for i, file_group in enumerate(batches):
            executor.submit(producer_task, batch_id, i+1, file_group, output_folder, queue)
    # 4. 多余文件处理
    move_extra_files(extra_files, NEXT_BATCH_FOLDER)

if __name__ == "__main__":
    main()