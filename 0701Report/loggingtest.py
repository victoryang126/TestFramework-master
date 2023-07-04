import logging

# 创建Logger对象
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 创建StreamHandler并设置刷新间隔为0
handler = logging.StreamHandler()
handler.flush = lambda: None
logger.addHandler(handler)

# 输出日志消息
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
