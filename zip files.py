import os
import zipfile
from concurrent.futures import ThreadPoolExecutor

MAX_ZIP_SIZE = 4 * 1024 * 1024 * 1024  # 4GB

def get_file_size(file_path):
    return os.path.getsize(file_path)

def group_files_by_size(file_list, max_size):
    groups = []
    current_group = []
    current_size = 0
    for file in file_list:
        size = get_file_size(file)
        if current_size + size > max_size and current_group:
            groups.append(current_group)
            current_group = []
            current_size = 0
        current_group.append(file)
        current_size += size
    if current_group:
        groups.append(current_group)
    return groups

def zip_files(file_group, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_group:
            zipf.write(file, arcname=os.path.basename(file))
    print(f"{zip_name} created.")

def main(file_list, output_dir, max_workers=4):
    groups = group_files_by_size(file_list, MAX_ZIP_SIZE)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for idx, group in enumerate(groups):
            zip_name = os.path.join(output_dir, f'archive_part{idx+1}.zip')
            executor.submit(zip_files, group, zip_name)

if __name__ == "__main__":
    # 这里替换成你自己的文件列表和输出目录
    files = [
        'file1.txt', 'file2.txt', 'file3.txt',  # ...
    ]
    output_directory = './output'
    os.makedirs(output_directory, exist_ok=True)
    main(files, output_directory)