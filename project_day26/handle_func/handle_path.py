import os
# 获取当前文件的根目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASE_DIR=os.path.join(BASE_DIR,'test_case')
REPORT_DIR=os.path.join(BASE_DIR,'test_report')
LOG_DIR=os.path.join(BASE_DIR,'test_log')
DATA_DIR=os.path.join(BASE_DIR,'test_data')
CONF_DIR=os.path.join(BASE_DIR,'config')


