from handle_func.handle_excel import handle_excel_class
from handle_func.handle_path import DATA_DIR
import os
import requests
from handle_func.handle_log import  log
from handle_func.handle_config import conf
import random
from comm_modul import myddt
import unittest
from handle_func.handle_db import db

@myddt.ddt
class test_register_class(unittest.TestCase):
    excel=handle_excel_class(os.path.join(DATA_DIR,'register_login.xlsx'),'register')
    case=excel.read_excel()
    @myddt.data(*case)
    def test_register(self,case):
        headers = eval(conf.get("header", "headers"))
        url=conf.get("address","url")+case['url']
        phone=self.random_phone()
        if "$phone$" in case['params']:
            case['params'] = case['params'].replace("$phone$", phone)
        params=eval(case['params'])
        expected=eval(case['expected'])
        methods=case['methods']
        rows=case['case_id']+1
        response=requests.request(url=url,json=params,method=methods,headers=headers)
        result=response.json()

        try:
            self.assertEqual(expected['code'],result['code'])
            self.assertEqual(expected['msg'],result['msg'])
            sql=case['mysql_data']
            if sql:
                response=db.find_data(sql.format(params['mobile_phone']))
                self.assertTrue(response)
        except Exception as E:
            self.excel.write_excel(row=rows,column=7,value="失败")
            log.error(f"{case['title']}执行失败")
            log.exception(E)
            raise E
        else:
            self.excel.write_excel(row=rows,column=7,value='通过')
            log.info(f"{case['title']}执行通过")

    @staticmethod
    def random_phone():
        while True:
            phone="131"
            for i in range(8):
                i = random.randint(0, 9)
                phone = phone + str(i)
            sql="select * from futureloan.member where mobile_phone={}".format(phone)
            res=db.find_data(sql)
            if not res:
                # print(phone)
                return phone