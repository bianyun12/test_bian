import os
import unittest
from comm_modul import myddt
from handle_func.handle_excel import handle_excel_class
# import os
from handle_func.handle_path import DATA_DIR
from handle_func.handle_config import conf
import requests
import logging
from handle_func.handle_log import log
from jsonpath import jsonpath
from handle_func.handle_db import db
from handle_func.handle_regular import handle_regular_class

@myddt.ddt
class test_withdraw_class(unittest.TestCase):
    excel=handle_excel_class(os.path.join(DATA_DIR,'register_login.xlsx'),'withdraw')
    case=excel.read_excel()
    @classmethod
    def setUpClass(cls):
        url=conf.get("address",'url')+'/member/login'
        params={"mobile_phone":conf.get("test_data","mobile"),
                "pwd":conf.get("test_data","pwd")
        }
        headers=eval(conf.get("headerv2","headers"))
        response_1=requests.request(url=url,method="post",json=params,headers=headers)
        res_1=response_1.json()
        token=jsonpath(res_1,"$..token")[0]
        cls.token = "Bearer" + " " + token
        cls.member_id=jsonpath(res_1,"$..id")[0]
    @myddt.data(*case)
    def test_withdraw(self,case):
        url=conf.get("address","url")+case['url']
        # print(url)
        # if "#member_id#" in case['params']:
        #     case['params']=case['params'].replace("#member_id#",str(self.member_id))
        #     print(self.member_id)
        case['params']=handle_regular_class.replace_data(case['params'],test_withdraw_class)
        params=eval(case['params'])
        methods=case['methods']
        headers=eval(conf.get("headerv2","headers"))
        headers['Authorization']=self.token
        expected=eval(case["expected"])
        rows=case['case_id']+1
        sql=case['check_data']
        # print(params['amount'])
        if sql:
            s_result=db.find_data(sql.format(self.member_id))
            s_amount=s_result[0]['leave_amount']
            # print(s_amount)

        response=requests.request(url=url,json=params,headers=headers,method=methods)
        res=response.json()

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if sql:
                e_result = db.find_data(sql.format(self.member_id))
                e_amount = e_result[0]['leave_amount']
                self.assertEqual(float(s_amount-e_amount),params['amount'])
        except AssertionError as e:
            self.excel.write_excel(row=rows,column=8,value='失败')
            self.excel.write_excel(row=rows,column=10,value=res['msg'])
            log.error(f"用例{case['title']}执行失败")
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=rows,column=8,value='通过')

