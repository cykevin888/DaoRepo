import threading
import time
import logging
from producer import FileCompressor
from consumer import Consumer

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数：集成生产者和消费者"""
    
    # 示例数据 - 你可以根据实际情况修改这些参数
    batch_ids = ["batch_001", "batch_002"]
    source_folders = [
        r"C:\Users\PC\AppData\Local\Temp\tmpl22x51pi\source1",
        r"C:\Users\PC\AppData\Local\Temp\tmpl22x51pi\source2",
        # r"C:\Users\PC\AppData\Local\Temp\tmpl22x51pi\source3"
    ]
    output_folders = [
        r"C:\Users\PC\AppData\Local\Temp\tmpl22x51pi\target1",
        r"C:\Users\PC\AppData\Local\Temp\tmpl22x51pi\target2",
        # r"C:\Users\PC\AppData\Local\Temp\tmpl22x51pi\target3"
    ]
    
    # 创建生产者（文件压缩器）
    producer = FileCompressor()
    
    # 创建消费者
    consumer = Consumer()
    
    # 创建生产者完成事件
    producer_completed_event = threading.Event()
    
    # 启动消费者线程
    compressed_files_queue = producer.get_queue()
    consumer.start_consuming(compressed_files_queue, producer_completed_event)
    
    try:
        # 启动生产者（压缩文件）
        logger.info("开始生产者任务...")
        producer.compress_files(batch_ids, source_folders, output_folders)
        
        # 标记生产者已完成
        producer_completed_event.set()
        logger.info("生产者已完成所有任务")
        
        # 等待队列中的所有任务被消费
        compressed_files_queue.join()
        logger.info("队列中的所有任务已被消费")
        
        # 停止消费者
        consumer.stop()
        
        # 输出统计信息
        processed_count = consumer.get_processed_count()
        logger.info(f"处理完成！总共处理了 {processed_count} 个压缩文件")
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在停止...")
        producer_completed_event.set()
        consumer.stop()
    except Exception as e:
        logger.error(f"程序执行过程中发生错误: {e}")
        producer_completed_event.set()
        consumer.stop()
        raise

if __name__ == "__main__":
    main()