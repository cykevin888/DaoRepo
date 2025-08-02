import os
import zipfile
import time
import logging
from queue import Queue, Empty
import threading
from concurrent.futures import ThreadPoolExecutor

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self):
        self.processed_count = 0
        self.lock = threading.Lock()
    
    def process_compressed_file(self, file_path):
        """
        处理压缩文件的示例函数
        这里可以替换为实际的处理逻辑
        """
        try:
            logger.info(f"开始处理压缩文件: {file_path}")
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                return False
            
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            logger.info(f"文件大小: {file_size / (1024):.2f} KB")
            
            # 模拟处理时间
            time.sleep(10)
            
            # 这里可以添加实际的文件处理逻辑
            # 例如：解压、分析、转换等
            
            # 模拟处理结果
            with self.lock:
                self.processed_count += 1
            
            logger.info(f"成功处理文件: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"处理文件 {file_path} 时发生错误: {e}")
            return False
    
    def get_processed_count(self):
        """获取已处理的文件数量"""
        return self.processed_count

class Consumer:
    def __init__(self, processor=None, max_workers=4):
        self.processor = processor or FileProcessor()
        self.running = False
        self.thread = None
        self.max_workers = max_workers
        self.executor = None
    
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
                    future = executor.submit(self.processor.process_compressed_file, file_path)
                    futures.append((future, file_path, compressed_files_queue))
                    
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
                        logger.info(f"文件处理成功: {file_path}")
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

# # 示例使用
# if __name__ == "__main__":
#     # 创建测试队列
#     test_queue = Queue()
#     test_queue.put(r"C:\temp\test.zip")
#
#     # 创建生产者完成事件
#     producer_completed = threading.Event()
#
#     # 创建消费者
#     consumer = Consumer()
#     consumer.start_consuming(test_queue, producer_completed)
#
#     # 模拟生产者完成
#     time.sleep(2)
#     producer_completed.set()
#
#     # 等待消费者完成
#     consumer.stop()
#     print(f"处理了 {consumer.get_processed_count()} 个文件")