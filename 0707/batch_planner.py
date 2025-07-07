import sys
from datetime import datetime, timedelta
import os

def get_batch_info(n_batches: int, now: datetime = None):
    if now is None:
        now = datetime.now()
    # 一天的总分钟数
    total_minutes = 24 * 60
    # 每个batch的分钟数
    batch_minutes = total_minutes // n_batches
    # 今天0点
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # 当前是今天的第几个分钟
    minutes_since_start = int((now - today_start).total_seconds() // 60)
    # 当前属于第几个batch（1-based）
    batch_no = minutes_since_start // batch_minutes + 1
    if batch_no > n_batches:
        batch_no = n_batches  # 防止极端情况溢出
    # 生成batch_id
    batch_id = f"{now.strftime('%Y%m%d')}_{batch_no:02d}"
    return now.date(), batch_no, batch_id

def get_next_batch(date: datetime.date, batch_no: int, n_batches: int):
    if batch_no < n_batches:
        next_batch_no = batch_no + 1
        next_date = date
    else:
        next_batch_no = 1
        next_date = date + timedelta(days=1)
    batch_id = f"{next_date.strftime('%Y%m%d')}_{next_batch_no:02d}"
    return next_date, next_batch_no, batch_id

def get_prev_batch(date: datetime.date, batch_no: int, n_batches: int):
    if batch_no > 1:
        prev_batch_no = batch_no - 1
        prev_date = date
    else:
        prev_batch_no = n_batches
        prev_date = date - timedelta(days=1)
    batch_id = f"{prev_date.strftime('%Y%m%d')}_{prev_batch_no:02d}"
    return prev_date, prev_batch_no, batch_id

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

if __name__ == "__main__":
    # 支持命令行参数传入batch数
    n_batches = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    date, batch_no, batch_id = get_batch_info(n_batches)
    print(f"当前: {date} 第{batch_no}个batch, batch_id: {batch_id}")

    next_date, next_batch_no, next_batch_id = get_next_batch(date, batch_no, n_batches)
    print(f"下一个: {next_date} 第{next_batch_no}个batch, batch_id: {next_batch_id}")

    prev_date, prev_batch_no, prev_batch_id = get_prev_batch(date, batch_no, n_batches)
    print(f"上一个: {prev_date} 第{prev_batch_no}个batch, batch_id: {prev_batch_id}")