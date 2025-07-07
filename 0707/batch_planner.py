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


def get_next_batch_id(current_batch_id: str, n_batches: int) -> str:
    """
    输入当前batch_id（如'20240708_03'）和n_batches，返回下一个batch_id，支持跨日期。
    """
    import datetime
    date_str, batch_no_str = current_batch_id.split('_')
    date = datetime.datetime.strptime(date_str, '%Y%m%d').date()
    batch_no = int(batch_no_str)
    next_date, next_batch_no, next_batch_id = get_next_batch(date, batch_no, n_batches)
    return next_batch_id

def get_prev_batch_id(current_batch_id: str, n_batches: int) -> str:
    """
    输入当前batch_id（如'20240708_03'）和n_batches，返回上一个batch_id，支持跨日期。
    """
    import datetime
    date_str, batch_no_str = current_batch_id.split('_')
    date = datetime.datetime.strptime(date_str, '%Y%m%d').date()
    batch_no = int(batch_no_str)
    prev_date, prev_batch_no, prev_batch_id = get_prev_batch(date, batch_no, n_batches)
    return prev_batch_id

if __name__ == "__main__":
    # 支持命令行参数传入batch数
    n_batches = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    date, batch_no, batch_id = get_batch_info(n_batches)
    print(f"当前: {date} 第{batch_no}个batch, batch_id: {batch_id}")

    next_date, next_batch_no, next_batch_id = get_next_batch(date, batch_no, n_batches)
    print(f"下一个: {next_date} 第{next_batch_no}个batch, batch_id: {next_batch_id}")

    prev_date, prev_batch_no, prev_batch_id = get_prev_batch(date, batch_no, n_batches)
    print(f"上一个: {prev_date} 第{prev_batch_no}个batch, batch_id: {prev_batch_id}")