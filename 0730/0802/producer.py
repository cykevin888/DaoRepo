import os
import zipfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FileCompressor:
    def __init__(self, max_size_kb=16):
        self.max_size_bytes = max_size_kb * 1024  # 转换为字节
        self.compressed_files_queue = Queue()
        self.task_counter = 0
        self.total_tasks = 0
        self.lock = threading.Lock()
    
    def compress_files(self, batch_ids, source_folders, output_folders, max_workers=4):
        """
        压缩文件的主函数
        
        Args:
            batch_ids: 批次ID列表
            source_folders: 源文件夹列表
            output_folders: 输出文件夹列表
            max_workers: 线程池最大工作线程数
        """
        if not (len(batch_ids) == len(source_folders) == len(output_folders)):
            raise ValueError("batch_ids, source_folders, output_folders 的长度必须相等")
        
        self.total_tasks = len(batch_ids)
        logger.info(f"开始处理 {self.total_tasks} 个批次")

        # 使用线程池处理每个批次
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for i in range(len(batch_ids)):
                future = executor.submit(
                    self._compress_batch,
                    batch_ids[i],
                    source_folders[i],
                    output_folders[i]
                )
                futures.append(future)
            
            # 等待所有任务完成
            for future in futures:
                future.result()
        
        logger.info("所有压缩任务完成")
    
    def _compress_batch(self, batch_id, source_folder, output_folder):
        """压缩单个批次的文件"""
        try:
            # 确保输出文件夹存在
            os.makedirs(output_folder, exist_ok=True)
            
            # 获取源文件夹中的所有文件
            files = []
            for filename in os.listdir(source_folder):
                if filename.endswith(('.wav', '.json')):
                    files.append(os.path.join(source_folder, filename))
            
            if not files:
                logger.warning(f"批次 {batch_id} 的源文件夹中没有找到文件")
                return
            
            # 按文件名分组（去掉扩展名）
            file_groups = {}
            for file_path in files:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                if base_name not in file_groups:
                    file_groups[base_name] = []
                file_groups[base_name].append(file_path)
            
            # 按16G一组进行压缩
            file_counter = 1
            current_group_size = 0
            
            # 创建第一个压缩文件
            zip_filename = f"{batch_id}_{file_counter:02d}.zip"
            current_zip_path = os.path.join(output_folder, zip_filename)
            current_zip = zipfile.ZipFile(current_zip_path, 'w', zipfile.ZIP_DEFLATED)
            logger.info(f"创建第一个压缩文件: {current_zip_path}")
            
            for group_name, group_files in file_groups.items():
                # 计算当前组文件的总大小
                group_size = sum(os.path.getsize(f) for f in group_files)
                
                # 检查当前组大小 + 新组大小是否会超过16KB
                if current_group_size + group_size > self.max_size_bytes:
                    # 关闭之前的压缩文件
                    if current_zip:
                        current_zip.close()
                        # 将压缩文件路径放入队列
                        self.compressed_files_queue.put(current_zip_path)
                        compressed_size = os.path.getsize(current_zip_path)
                        logger.info(f"完成压缩文件: {current_zip_path} (原始文件大小: {current_group_size / 1024:.2f} KB, 压缩后大小: {compressed_size / 1024:.2f} KB)")
                        

                    
                    # 创建新的压缩文件
                    file_counter += 1
                    zip_filename = f"{batch_id}_{file_counter:02d}.zip"
                    current_zip_path = os.path.join(output_folder, zip_filename)
                    current_zip = zipfile.ZipFile(current_zip_path, 'w', zipfile.ZIP_DEFLATED)
                    logger.info(f"创建新的压缩文件: {current_zip_path}")
                    current_group_size = 0
                
                # 添加文件到压缩包
                for file_path in group_files:
                    arc_name = os.path.basename(file_path)
                    current_zip.write(file_path, arc_name)
                    logger.debug(f"添加文件到压缩包: {file_path}")

                # 模拟
                time.sleep(10)
                
                # 更新当前组大小
                current_group_size += group_size


            
            # 关闭最后一个压缩文件
            if current_zip:
                current_zip.close()
                self.compressed_files_queue.put(current_zip_path)
                compressed_size = os.path.getsize(current_zip_path)
                logger.info(f"完成压缩文件: {current_zip_path} (原始文件大小: {current_group_size / 1024:.2f} KB, 压缩后大小: {compressed_size / 1024:.2f} KB)")

            
            # 更新任务计数器
            with self.lock:
                self.task_counter += 1
                logger.info(f"批次 {batch_id} 完成，进度: {self.task_counter}/{self.total_tasks}")
                
        except Exception as e:
            logger.error(f"压缩批次 {batch_id} 时发生错误: {e}")
            raise
    
    def is_all_tasks_completed(self):
        """检查是否所有任务都已完成"""
        return self.task_counter >= self.total_tasks
    
    def get_queue(self):
        """获取压缩文件队列"""
        return self.compressed_files_queue

# 示例使用
if __name__ == "__main__":
    # 示例数据
    batch_ids = ["batch_001", "batch_002", "batch_003"]
    source_folders = [
        "source1",
        "source2",
        "source3"
    ]
    output_folders = [
        "target1",
        "target2",
        "target3"
    ]
    
    compressor = FileCompressor(max_size_kb=16)
    compressor.compress_files(batch_ids, source_folders, output_folders)