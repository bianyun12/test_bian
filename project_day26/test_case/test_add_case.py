import unittest
from comm_modul import myddt
from handle_func.handle_excel import handle_excel_class
import os
from handle_func.handle_path import DATA_DIR
from handle_func.handle_config import conf
import requests
from jsonpath import jsonpath
from handle_func.handle_log import log
from handle_func.handle_db import db
from handle_func.handle_regular import handle_regular_class
@myddt.ddt
class test_add_class(unittest.TestCase):
    excel=handle_excel_class(os.path.join(DATA_DIR,"register_login.xlsx"),"add")
    case=excel.read_excel()
    @classmethod
    def setUpClass(cls):
        url = conf.get("address", 'url') + '/member/login'
        params = {"mobile_phone": conf.get("test_data", "mobile"),
                  "pwd": conf.get("test_data", "pwd")
                  }
        headers = eval(conf.get("headerv2", "headers"))
        response_login = requests.request(url=url, method="post", json=params, headers=headers)
        res_login=response_login.json()
        # print(res_login)
        cls.token="Bearer"+" "+jsonpath(res_login,"$..token")[0]
        cls.member_id=jsonpath(res_login,"$..id")[0]
    @myddt.data(*case)
    def test_add(self,item):
        url=conf.get("address",'url')+item['url']
        # if "#member_id#" in item['params']:
        #     print(self.member_id)
        #     item['params']=item['params'].replace("#member_id#",str(self.member_id))
        item['params']=handle_regular_class.replace_data(item['params'],test_add_class)
        params=eval(item['params'])
        headers=eval(conf.get("headerv2","headers"))
        headers["Authorization"]=self.token
        methods=item['methods']
        expected=eval(item['expected'])
        rows=item['case_id']+1
        sql=item['check_data']
        if sql:
            s_res=db.find_data(sql.format(self.member_id))
            s_num=s_res[0]['num']
            print(s_num)

        response_add=requests.request(url=url,json=params,method=methods,headers=headers)
        res_add=response_add.json()
        if sql:
            e_res=db.find_data(sql.format(self.member_id))
            e_num=e_res[0]['num']
            # print(e_num)
        # print(res_add)
        print("预期结果：",expected)
        print("实际结果：",res_add)
        try:
            self.assertEqual(expected['code'],res_add['code'])
            self.assertEqual(expected['msg'], res_add['msg'])
            if sql:
                self.assertEqual(int(e_num-s_num),1)

        except AssertionError as e:
            self.excel.write_excel(row=rows,column=8,value="fail")
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=rows,column=8,value="pass")

