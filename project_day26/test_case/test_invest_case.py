# 1.先登录
# 2.先新增项目
# 3.审核项目
# 4.投资项目
# 问题一：不知道怎么实现多表查询
# 问题二：参数里如何实现动态变量获取
# 问题三：前置接口的变量如何获取excel用例的数据
import unittest
from comm_modul import myddt
from handle_func.handle_config import conf
import requests
from jsonpath import jsonpath
from handle_func.handle_excel import handle_excel_class
import os
from handle_func.handle_path import DATA_DIR
from handle_func.handle_regular import handle_regular_class
from handle_func.handle_log import log
@myddt.ddt
class test_invest_class(unittest.TestCase):
    excel=handle_excel_class(os.path.join(DATA_DIR,"register_login.xlsx"),'invest')
    case=excel.read_excel()
    # print(case)
    @classmethod
    def setUpClass(cls):
        # ----------------------------普通会员登录-----------------------------------
        url=conf.get("address","url")+"/member/login"
        params={"mobile_phone":conf.get("test_data","mobile"),
                "pwd":conf.get("test_data","pwd")
        }
        headers=eval(conf.get("headerv2","headers"))
        login_response=requests.request(url=url,headers=headers,json=params,method="post")
        login_result=login_response.json()
        cls.token="Bearer"+" "+jsonpath(login_result,"$..token")[0]
        cls.member_id=jsonpath(login_result,"$..id")[0]
        # -------------------------------管理员登录----------------------------------
        url = conf.get("address", 'url') + '/member/login'
        admin_params = {"mobile_phone": conf.get("test_data", "admin_mobile"),
                        "pwd": conf.get("test_data", "admin_pwd")
                        }
        headers = eval(conf.get("headerv2", "headers"))
        admin_response_login = requests.request(url=url, method="post", json=admin_params, headers=headers)
        admin_res_login = admin_response_login.json()
        # print(admin_res_login)

        cls.admin_token = "Bearer" + " " + jsonpath(admin_res_login, "$..token")[0]
        # print(cls.admin_token)

    def setUp(self):
        url=conf.get("address","url")+"/loan/add"
        params={
            "member_id": self.member_id,
            "title": "dklf",
            "amount": "200",
            "loan_rate": 12.7,
            "loan_term": 9,
            "loan_date_type": 1,
            "bidding_days": 5

        }
        headers=eval(conf.get("headerv2","headers"))
        headers['Authorization']=self.token
        add_response=requests.request(url=url,json=params,method="post",headers=headers)
        add_result=add_response.json()
        test_invest_class.loan_id=jsonpath(add_result,"$..id")[0]
        url=conf.get("address","url")+"/loan/audit"

        params={"loan_id":self.loan_id,
                "approved_or_not":self.case[0]['status']

        }
        print(params)
        headers['Authorization'] = self.admin_token
        audit_response=requests.request(url=url,json=params,method="PATCH",headers=headers)
        audit_result=audit_response.json()
        print(audit_result)
    @myddt.data(*case)
    def test_invest(self,item):
        url=conf.get("address",'url')+item['url']
        item['params']=handle_regular_class.replace_data(item['params'],test_invest_class)
        params=eval(item['params'])
        methods=item['methods']
        rows=item['case_id']+1
        headers=eval(conf.get("headerv2","headers"))
        headers['Authorization']=self.token
        expected=eval(item['expected'])
        invest_response=requests.request(url=url,json=params,method=methods,headers=headers)
        invest_result=invest_response.json()
        print("预期结果为：",expected)
        print("实际结果为：",invest_result)
        try:
            self.assertEqual(expected['code'],invest_result['code'])
            self.assertEqual(expected['msg'],invest_result['msg'])
        except AssertionError as e:
            self.excel.write_excel(row=rows,column=10,value="fail")
            log.exception(e)
            raise e
        else:
            self.excel.write_excel(row=rows,column=10,value="pass")
