# coding: utf-8

# # 用户名:cf_chinascope
# # 密码:zKqVjm
# # http://106.ihuyi.cn/webservice/sms.php?method=Submit
# # 接口说明
# # 类型    参数名称    参数值描述
# # 参数    method      Submit
# # 参数    account     提交账户名
# # 参数    password    提交账户密码 （采用MD5加密）
# # 参数    mobile      接收手机号码，只能提交1个号码
# # 参数    content     短信内容（支持300个字的长短信，长短信按多条计费）
#
# # 神盾局OPS系统：前方英雄【%s】即将在【%s】过期，请及时充能！！
#
# import bmp.utils.sms as sms
# from bmp.tasks.sms.base import BaseSms
# from bmp.models.user import Group
# from bmp.const import DEFAULT_GROUP
#
# class SmsAlert(BaseSms):
#     def sendg(self,title,expire_time,lead_times):
#         content="前方英雄【%s】即将在【%s】过期，请及时充能！！"%(title,expire_time.strftime("%Y-%m-%d"))
#         mobiles=[u for u in Group.get_users(DEFAULT_GROUP.SMS.ALERT)]
#         for mobile in mobiles:
#             for lead_time in lead_times:
#                 self.add_job(sms.send, args=(mobile, content), date=expire_time-lead_time)


#告警
class Alert:
    pass



if __name__ == "__main__":
    pass









class Alert():
    def __init__(self):
        pass




