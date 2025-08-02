import os
import zipfile
import time
import logging
import shutil
from queue import Queue, Empty
import threading
from concurrent.futures import ThreadPoolExecutor
import paramiko

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class FileProcessor:
    def __init__(self, remote_paths=["/tmp/remote1", "/tmp/remote2", "/tmp/remote3", "/tmp/remote4"], max_retries=3, sftp_config=None):
        self.processed_count = 0
        self.lock = threading.Lock()
        self.remote_paths = remote_paths
        self.max_retries = max_retries
        self.sftp_config = sftp_config or {
            'hostname': 'localhost',
            'username': 'user',
            'password': 'password',
            'port': 22
        }
    
    def get_remote_path(self, file_path, batch_no):
        """根据batch_no和文件名中的n选择远程路径"""
        filename = os.path.basename(file_path)
        try:
            # 提取batchid_n.zip中的n
            n = int(filename.split('_')[1].split('.')[0])
            # 先根据batch_no选择两个路径
            if batch_no % 2 == 0:
                selected_paths = [self.remote_paths[0], self.remote_paths[1]]
            else:
                selected_paths = [self.remote_paths[2], self.remote_paths[3]]
            # 再根据n选择其中一个
            return selected_paths[n % 2]
        except:
            # 如果无法解析，使用默认路径
            return self.remote_paths[0]

    def upload_file(self, file_path, batch_no):
        """通过SFTP上传文件到远程路径"""
        try:
            filename = os.path.basename(file_path)
            remote_path = self.get_remote_path(file_path, batch_no)
            remote_file_path = f"{remote_path}/{filename}"
            
            # 创建SSH客户端
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(**self.sftp_config)
            
            # 创建SFTP客户端
            sftp = ssh.open_sftp()
            
            # 检查远程目录是否存在，不存在则创建
            try:
                sftp.stat(remote_path)
            except FileNotFoundError:
                sftp.mkdir(remote_path)
            
            # 上传文件
            sftp.put(file_path, remote_file_path)
            
            sftp.close()
            ssh.close()
            
            logger.info(f"文件SFTP上传成功: {file_path} -> {remote_file_path}")
            return True
        except Exception as e:
            logger.error(f"文件SFTP上传失败: {file_path}, 错误: {e}")
            return False

    def process_compressed_file(self, file_path, batch_no=2):
        """
        处理压缩文件的示例函数
        这里可以替换为实际的处理逻辑
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"开始处理压缩文件 (尝试 {attempt + 1}/{self.max_retries}): {file_path}, batch_no: {batch_no}")
                
                # 检查文件是否已存在于远程路径
                filename = os.path.basename(file_path)
                remote_path = self.get_remote_path(file_path, batch_no)
                remote_file_path = f"{remote_path}/{filename}"
                
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(**self.sftp_config)
                    sftp = ssh.open_sftp()
                    sftp.stat(remote_file_path)
                    sftp.close()
                    ssh.close()
                    logger.info(f"文件已存在于远程路径，跳过处理: {remote_file_path}")
                    with self.lock:
                        self.processed_count += 1
                    return True
                except FileNotFoundError:
                    pass

                # 检查文件是否存在
                if not os.path.exists(file_path):
                    raise Exception(f"文件不存在: {file_path}")


                # 上传文件到远程路径
                if not self.upload_file(file_path, batch_no):
                    raise Exception("文件上传失败")

                # 模拟处理时间
                time.sleep(10)


                # 模拟处理结果
                with self.lock:
                    self.processed_count += 1

                logger.info(f"成功处理文件: {file_path}")
                return True

            except Exception as e:
                logger.error(f"处理文件 {file_path} 时发生错误 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"等待重试...")
                    time.sleep(2)
                else:
                    logger.error(f"文件处理失败，已达到最大重试次数: {file_path}")
                    return False

    def get_processed_count(self):
        """获取已处理的文件数量"""
        return self.processed_count


class Consumer:
    def __init__(self, processor=None, max_workers=4, remote_paths=["/tmp/remote1", "/tmp/remote2", "/tmp/remote3", "/tmp/remote4"], max_retries=3, sftp_config=None):
        self.processor = processor or FileProcessor(remote_paths, max_retries, sftp_config)
        self.running = False
        self.thread = None
        self.max_workers = max_workers
        self.executor = None
        self.batch_no = 0

    def start_consuming(self, compressed_files_queue, producer_completed_event):
        """
        开始消费队列中的文件

        Args:
            compressed_files_queue: 压缩文件队列
            producer_completed_event: 生产者完成事件
        """
        self.running = True
        self.thread = threading.Thread(
            target=self._consume_loop,
            args=(compressed_files_queue, producer_completed_event)
        )
        self.thread.start()
        logger.info("消费者线程已启动")

    def _consume_loop(self, compressed_files_queue, producer_completed_event):
        """消费循环"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            self.executor = executor
            futures = []

            while self.running:
                try:
                    # 尝试从队列获取文件路径，超时1秒
                    file_path = compressed_files_queue.get(timeout=1)
                    logger.info(f"从队列获取到文件: {file_path}")

                    # 提交到线程池处理
                    future = executor.submit(self.processor.process_compressed_file, file_path, self.batch_no)
                    futures.append((future, file_path, compressed_files_queue))
                    self.batch_no += 1

                except Empty:
                    # 队列为空，检查生产者是否已完成
                    if producer_completed_event.is_set():
                        logger.info("生产者已完成且队列为空，等待剩余任务完成")
                        break
                    else:
                        logger.debug("队列暂时为空，等待更多文件...")
                        continue
                except Exception as e:
                    logger.error(f"消费过程中发生错误: {e}")
                    break

            # 等待所有任务完成
            for future, file_path, queue in futures:
                try:
                    success = future.result()
                    if success:
                        pass
                    else:
                        logger.warning(f"文件处理失败: {file_path}")
                    queue.task_done()
                except Exception as e:
                    logger.error(f"处理文件 {file_path} 时发生错误: {e}")
                    queue.task_done()

        logger.info("消费者线程结束")

    def stop(self):
        """停止消费者"""
        self.running = False
        if self.executor:
            self.executor.shutdown(wait=True)
        if self.thread and self.thread.is_alive():
            self.thread.join()
        logger.info("消费者已停止")

    def get_processed_count(self):
        """获取已处理的文件数量"""
        return self.processor.get_processed_count()

# 示例使用
if __name__ == "__main__":
    # 创建测试队列
    test_queue = Queue()
    # 测试重试：使用不存在的文件路径
    test_queue.put(r"C:\temp\nonexistent.zip")

    # 创建生产者完成事件
    producer_completed = threading.Event()

    # 创建消费者
    consumer = Consumer()
    consumer.start_consuming(test_queue, producer_completed)

    # 模拟生产者完成
    time.sleep(2)
    producer_completed.set()

    # 等待消费者完成
    consumer.stop()
    print(f"处理了 {consumer.get_processed_count()} 个文件")