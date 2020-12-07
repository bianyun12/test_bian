# 注册、登录、充值
# 注册一组账号保存到配置文件，账号为随机数生成
from random import randint
import random

from handle_func.handle_config import conf
from handle_func.handle_db import db
import requests
from jsonpath import jsonpath
# 随机生成手机号，方便注册用
def random_phone():
    while True:
        phone = "131"
        for i in range(8):
            i = random.randint(0, 9)
            phone = phone + str(i)
        sql = "select * from futureloan.member where mobile_phone={}".format(phone)
        res = db.find_data(sql)
        if not res:
            # print(phone)
            return phone



def pre_handle():
    register_url=conf.get("address","url")+"/member/register"
    register_params={"mobile_phone":random_phone(),
            "pwd":12345678
    }
    headers=eval(conf.get("headerv2","headers"))
    register_response=requests.request(url=register_url,json=register_params,method="post",headers=headers)
    register_result=register_response.json()
    # 判断是否注册成功，如果账号注册成功，写入账号到配置文件中，并进行登录操作
    if register_result['code']==0:
        # 把账号写入config文件中

        conf.write_config('test_data','mobile',str(register_params['mobile_phone']))
        conf.write_config("test_data","pwd",str(register_params['pwd']))
        # 进行登录操作
        login_url = conf.get("address", "url") + "/member/login"
        login_params = {"mobile_phone": conf.get("test_data","mobile"),
                  "pwd": conf.get("test_data","pwd")
                  }
        headers = eval(conf.get("headerv2", "headers"))
        login_response = requests.request(url=login_url, json=login_params, method="post", headers=headers)
        login_result = login_response.json()
        token="Bearer"+" "+jsonpath(login_result,"$..token")[0]
        member_id=jsonpath(login_result,"$..id")[0]
        #登录成功后进行充值
        if login_result['code']==0:
            recharge_url=conf.get("address","url")+"/member/recharge"
            headers["Authorization"]=token
            recharge_params={"member_id":member_id,
                    "amount":500000
            }
            requests.request(url=recharge_url,json=recharge_params,headers=headers,method="post")
            requests.request(url=recharge_url, json=recharge_params, headers=headers, method="post")
            requests.request(url=recharge_url, json=recharge_params, headers=headers, method="post")
        else:
            raise ValueError("初始化环境登录失败")
    else:
        raise ValueError("初始化环境注册失败！")
if __name__=="__main__":
    pre_handle()
