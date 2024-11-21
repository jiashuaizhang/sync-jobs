import time

from mysql import sync_mysql
import logging
from common import read_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

configs = read_config()

if __name__ == '__main__':
    logger = logging.getLogger("sync_main")
    interval = int(configs['sync.interval'])
    i = 0
    sync_mysql.init_config()
    while True:
        logger.info(f'同步任务开始，序号: {i}')
        try:
            sync_mysql.execute()
            logger.info(f'同步mysql完成，序号: {i}')
            # other jobs below
        except Exception as e:
            logger.error(f"同步异常: {e}")
        logger.info(f'同步任务结束，序号: {i}')
        time.sleep(interval * 60)
        i += 1
