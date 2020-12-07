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
class test_withdraw02_class(unittest.TestCase):
    excel=handle_excel_class(os.path.join(DATA_DIR,'register_login.xlsx'),'withdraw2')
    case=excel.read_excel()
    @myddt.data(*case)
    def test_withdraw02(self,case):

        url=conf.get("address","url")+case['url']
        # if "#mobile_phone#" in case['params']:
        #     case['params']=case['params'].replace("#mobile_phone#",conf.get("user","mobile_phone"))
        # if "#pwd#" in case['params']:
        #     case['params']=case['params'].replace("#pwd#",conf.get("user","pwd"))
        # if "#member_id#" in case['params']:
        #     case['params']=case['params'].replace("#member_id#",str(self.member_id))
        case['params']=handle_regular_class.replace_data(case['params'],test_withdraw02_class)
        params=eval(case['params'])
        # print(params)
        methods=case['methods']
        headers = eval(conf.get("headerv2", "headers"))
        if case['interface']=='withdraw':
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
        print("预期结果：",expected)
        print("实际结果：",res)
        # print(res)
        if case['interface']=="login":
            test_withdraw02_class.token="Bearer"+" "+jsonpath(res,"$..token")[0]
            test_withdraw02_class.member_id=jsonpath(res,"$..id")[0]
        if sql:
            e_result=db.find_data(sql.format(self.member_id))
            e_amount=e_result[0]['leave_amount']
            # print(e_amount)
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])
            if sql:
                self.assertEqual(float(s_amount-e_amount),float(params['amount']))
        except AssertionError as e:
            self.excel.write_excel(row=rows,column=8,value='失败')
            # self.excel.write_excel(row=rows,column=10,value=res['msg'])
            log.error(f"用例{case['title']}执行失败")
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=rows,column=8,value='通过')

