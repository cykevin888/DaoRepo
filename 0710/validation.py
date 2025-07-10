import os
import pandas as pd

def find_transaction_files(report_folder, source_folder):
    # 1. 读取report文件夹下的Excel文件
    excel_files = [f for f in os.listdir(report_folder) if f.endswith('.xlsx') or f.endswith('.xls')]
    if not excel_files:
        raise FileNotFoundError("report文件夹下没有Excel文件")
    report_path = os.path.join(report_folder, excel_files[0])
    df = pd.read_excel(report_path)

    # 2. 拿到status=success的transaction id列表
    success_ids = df[df['status'] == 'success']['transaction_id'].astype(str).tolist()

    # 3. 遍历source_folder下所有子目录，查找同名wav和json文件
    found_ids = set()
    id_to_files = {tid: {'wav': False, 'json': False} for tid in success_ids}

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            name, ext = os.path.splitext(file)
            if name in id_to_files:
                if ext.lower() == '.wav':
                    id_to_files[name]['wav'] = True
                elif ext.lower() == '.json':
                    id_to_files[name]['json'] = True

    # 4. 统计match的记录数
    match_count = 0
    unmatched_ids = []
    for tid, files in id_to_files.items():
        if files['wav'] and files['json']:
            match_count += 1
        else:
            unmatched_ids.append(tid)

    # 5. 返回结果
    return match_count, unmatched_ids

# 示例调用
report_folder = 'report'
source_folder = 'source_folder'
match_count, unmatched_ids = find_transaction_files(report_folder, source_folder)
print(f"匹配成功的记录数: {match_count}")
if unmatched_ids:
    print("未匹配的transaction_id列表:", unmatched_ids)
else:
    print("所有transaction_id都已匹配")