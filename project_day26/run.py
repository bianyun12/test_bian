from unittestreport import TestRunner
import unittest
from handle_func.handle_path import REPORT_DIR,CASE_DIR,CONF_DIR
from handle_func.handle_config import config,conf
from pre_func import pre_handle


suite=unittest.defaultTestLoader.discover(CASE_DIR)
pre_handle()
runner=TestRunner(suite,
                 filename=conf.get('report','report_name'),
                 report_dir=REPORT_DIR,
                 title=conf.get('report','title'),
                 tester=conf.get('report','taster'),
                 desc=conf.get('report','desc'),
                 templates=1)
runner.run()