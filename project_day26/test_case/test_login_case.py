import os
import unittest

import requests

from comm_modul import myddt
from handle_func.handle_config import conf
from handle_func.handle_excel import handle_excel_class
from handle_func.handle_log import log
from handle_func.handle_path import DATA_DIR


@myddt.ddt
class test_login_class(unittest.TestCase):
    excel=handle_excel_class(os.path.join(DATA_DIR,'register_login.xlsx'),'login')
    case=excel.read_excel()
    @myddt.data(*case)
    def test_login(self,case):
        headers = eval(conf.get("header", "headers"))
        url=conf.get("address","url")+case['url']
        params=eval(case['params'])
        methods=case['methods']
        expected=eval(case['expected'])
        rows=case['case_id']+1
        reponse=requests.request(url=url,method=methods,json=params,headers=headers)
        result=reponse.json()
        try:
            self.assertEqual(expected['code'],result['code'])
            self.assertEqual(expected['msg'],result['msg'])
        except Exception as E:
            self.excel.write_excel(row=rows,column=7,value="失败")
            log.error(f"{case['title']}执行失败")
            log.exception(E)
            raise E

        else:
            self.excel.write_excel(row=rows,column=7,value="通过")
            log.info(f"{case['title']}执行通过")