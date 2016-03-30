# coding: utf-8

# 用户名:cf_chinascope
# 密码:zKqVjm
# http://106.ihuyi.cn/webservice/sms.php?method=Submit
# 接口说明
# 类型    参数名称    参数值描述
# 参数    method      Submit
# 参数    account     提交账户名
# 参数    password    提交账户密码 （采用MD5加密）
# 参数    mobile      接收手机号码，只能提交1个号码
# 参数    content     短信内容（支持300个字的长短信，长短信按多条计费）

# 神盾局OPS系统：前方英雄【%s】即将在【%s】过期，请及时充能！！

import bmp.utils.sms as sms
from bmp import sched
from datetime import datetime,timedelta
from bmp import log

class BaseSms:
    def __send(self, mobile, content, date, _id,minutes):
        try:
            sms.send(mobile,content)
        except Exception,e:
            log.exception(e)
            if minutes < 12:
                minutes += 1
                sched.add_job(self.__send,
                              "date",
                              id=_id,
                              run_date=datetime.now() + timedelta(minutes=minutes),
                              args=(mobile, content, date, _id,minutes),
                              misfire_grace_time=60 * 60 * 24 * 365 * 100,
                              replace_existing=True)

    def send(self, mobiles, content, date=None, _id=None):
        for mobile in mobiles:
            if not _id:
                _id = "%s_%s_%s" % (mobile, content, date)

            minutes = int(1)
            sched.add_job(self.__send,
                          "date",
                          id=_id,
                          run_date=date,
                          misfire_grace_time=60 * 60 * 24 * 365 * 100,
                          args=(mobile, content, date, _id,minutes),
                          replace_existing=True)
