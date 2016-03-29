# coding=utf-8

# todo 神盾局OPS系统：前方英雄【变量】即将在【变量】过期，请及时充能！！

# 用户名:cf_chinascope
# 密码:zKqVjm



# http://106.ihuyi.cn/webservice/sms.php?method=Submit
# 接口说明
# 类型	参数名称	参数值描述
# 参数	method	Submit
# 参数	account	提交账户名
# 参数	password	提交账户密码 （采用MD5加密）
# 参数	mobile	接收手机号码，只能提交1个号码
# 参数	content	短信内容（支持300个字的长短信，长短信按多条计费）
import requests
import xml.dom.minidom as dom


def send(content):
    return requests.post(
        "http://106.ihuyi.cn/webservice/sms.php?method=Submit",
        {
            "account": "cf_chinascope",
            "password": "zKqVjm"
        }
    ).text.decode("utf8")

if __name__=="__main__":
    dd=dom.parseString(send("test"))
    print dd