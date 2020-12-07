import logging
from logging import Logger
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler
from handle_func.handle_path import LOG_DIR,CONF_DIR
import os
from handle_func.handle_config import config,conf
# 创建日志收集器
# config_path=os.path.join(CONF_DIR,'conf.ini')
# conf=config(config_path)
def create_log():
    # 第一步：创建一个收集器
    log=logging.getLogger('bian')
    # 为收集器设置收集等级
    log.setLevel(conf.get('logging','collect_leval'))
    # 第二步：创建一个输出到文件的输出渠道
    #创建文件输出渠道
    file_output=TimedRotatingFileHandler(os.path.join(LOG_DIR,'log.log'), when='s', interval=5, backupCount=2, encoding='utf-8')
    # 设置文件输出渠道输出的错误等级

    file_output.setLevel(conf.get("logging", 'file_output'))
    # 将设置好的文件输出渠道添加到收集器中
    log.addHandler(file_output)
    # 第三步：创建一个输出到控制台的输出渠道
    # 创建控制台输出渠道
    console_output=logging.StreamHandler()
    # 设置控制台输出等级
    log.setLevel(conf.get("logging",'console_output'))
    # 将设置好的输出渠道添加到收集器中
    log.addHandler(console_output)
    # 第四步：设置日志输出格式
    formater='%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
    mate=logging.Formatter(formater)
    file_output.setFormatter(mate)
    console_output.setFormatter(mate)
    return log

log: Logger=create_log()
