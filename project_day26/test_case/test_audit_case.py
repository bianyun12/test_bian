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
# 管理员登录、普通会员登录，普通会员新增项目、管理员审核项目
@myddt.ddt
class test_audit_class(unittest.TestCase):
    excel = handle_excel_class(os.path.join(DATA_DIR, "register_login.xlsx"), "audit")
    case = excel.read_excel()

    @classmethod
    def setUpClass(cls):
        # 第一步：-----------------------普通会员登录-----------------------------
        url = conf.get("address", 'url') + '/member/login'
        params = {"mobile_phone": conf.get("test_data", "mobile"),
                  "pwd": conf.get("test_data", "pwd")
                  }
        headers = eval(conf.get("headerv2", "headers"))
        response_login = requests.request(url=url, method="post", json=params, headers=headers)
        res_login = response_login.json()

        cls.token = "Bearer" + " " + jsonpath(res_login, "$..token")[0]
        cls.member_id = jsonpath(res_login, "$..id")[0]
        # 第二步：------------------------管理员登录------------------------------
        url = conf.get("address", 'url') + '/member/login'
        admin_params = {"mobile_phone": conf.get("test_data", "admin_mobile"),
                  "pwd": conf.get("test_data", "admin_pwd")
                  }
        headers = eval(conf.get("headerv2", "headers"))
        admin_response_login = requests.request(url=url, method="post", json=admin_params, headers=headers)
        admin_res_login = admin_response_login.json()
        print(admin_res_login)

        cls.admin_token="Bearer"+" "+jsonpath(admin_res_login,"$..token")[0]
        print(cls.admin_token)

    # 定义增加项目方法，每次执行审核方法之前执行该方法
    def setUp(self):

        url = conf.get("address", 'url') + '/loan/add'
        params = {
                "member_id": self.member_id,
                "title": "dklf",
                "amount": "100",
                "loan_rate": 12.7,
                "loan_term": 9,
                "loan_date_type": 1,
                "bidding_days": 5

            }
        headers = eval(conf.get("headerv2", "headers"))
        headers["Authorization"] = self.token

        response_add = requests.request(url=url, json=params, method="post", headers=headers)
        res_add = response_add.json()
        test_audit_class.loan_id = jsonpath(res_add, "$..id")[0]




    @myddt.data(*case)
    def test_audit(self,item):
        url = conf.get("address", 'url') + item['url']
        item['params']=handle_regular_class.replace_data(item['params'],test_audit_class)

        params = eval(item['params'])
        print(params)
        headers = eval(conf.get("headerv2", "headers"))
        headers["Authorization"] = self.admin_token
        methods = item['methods']
        expected = eval(item['expected'])
        rows = item['case_id'] + 1


        response_add = requests.request(url=url, json=params, method=methods, headers=headers)
        res_add = response_add.json()
        print("预期结果：", expected)
        print("实际结果：", res_add)
        sql=item['check_data']

        try:
            self.assertEqual(expected['code'], res_add['code'])
            self.assertEqual(expected['msg'], res_add['msg'])
            if sql:
                search = db.find_data(sql.format(self.loan_id))[0]['status']

                self.assertEqual(expected['status'],search)
                if int(search)==2:
                    test_audit_class.pass_loan_id = params['loan_id']



        except AssertionError as e:
            self.excel.write_excel(row=rows, column=8, value="fail")
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=rows, column=8, value="pass")




