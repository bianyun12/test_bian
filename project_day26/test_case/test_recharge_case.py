import decimal
import unittest
# from unicodedata import decimal

from comm_modul import myddt
from handle_func.handle_excel import handle_excel_class
from handle_func.handle_path import DATA_DIR
from handle_func.handle_config import conf
import requests
import os
from handle_func.handle_log import log
from jsonpath import jsonpath
from handle_func.handle_db import  db
@myddt.ddt
class test_recharge_calss(unittest.TestCase):
    excel=handle_excel_class(os.path.join(DATA_DIR,'register_login.xlsx'),'recharge')
    case=excel.read_excel()
    # 获取token以及member_id
    @classmethod
    def setUpClass(cls):
        url=conf.get("address","url")+'/member/login'
        params={"mobile_phone":conf.get("test_data","mobile"),
                "pwd":conf.get("test_data","pwd")
        }
        headers=eval(conf.get("headerv2","headers"))
        reponse=requests.request(url=url,method='post',json=params,headers=headers)
        res=reponse.json()
        token=jsonpath(res,"$..token")[0]
        cls.token="Bearer"+" "+token
        cls.member_id=jsonpath(res,"$..id")[0]

    @myddt.data(*case)
    def test_recharge(self,case):
        base_url=conf.get("address",'url')
        url=base_url+case['url']
        if "#member_id#" in case['params']:
            case['params']=case['params'].replace("#member_id#",str(self.member_id))
        params=eval(case['params'])
        methods=case['methods']
        headers=eval(conf.get("headerv2","headers"))
        headers['Authorization']=self.token
        expected=eval(case['expected'])
        rows=case['case_id']+1
        sql=case['check_data']
        if sql:
            s_result=db.find_data(sql.format(self.member_id))
            s_amout=s_result[0]["leave_amount"]
            # print(s_amout)
        response=requests.request(url=url,json=params,method=methods,headers=headers)
        res=response.json()
        print("预期结果：",expected)
        print("实际结果：",res)

        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if sql:
                e_result = db.find_data(sql.format(self.member_id))
                e_amout = e_result[0]["leave_amount"]
                self.assertEqual(float(e_amout-s_amout),params['amount'])
        except AssertionError as e:
            self.excel.write_excel(row=rows,column=7,value="失败")
            # self.excel.write_excel(row=rows,column=8,value=str(res['msg']))
            log.error(f"测试用例{case['title']}执行失败")
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=rows,column=7,value="通过")
            log.info(f"测试用例{case['title']}执行通过")


