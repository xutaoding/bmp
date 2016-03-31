# coding: utf-8
from apscheduler.jobstores.base import JobLookupError

from bmp.tasks.mail.base import BaseMail
from bmp.tasks.sms.base import BaseSms

from bmp.models.user import Group
from bmp.const import DEFAULT_GROUP
from bmp import app
from bmp.utils.exception import ExceptionEx
from bmp import log
import traceback


# 告警
class Alert(BaseSms, BaseMail):
    def add_all(self, name, objs, expire_time_field, lead_times):
        if not isinstance(objs, list):
            objs = [objs]

        for obj in objs:
            expire_time = getattr(obj, expire_time_field)
            self.add(name, obj, expire_time, lead_times)

    def add(self, name, obj, expire_time, lead_times):
        try:
            _id = "_".join([obj.__class__.__name__, str(obj.id)])

            if not isinstance(lead_times, list):
                lead_times = [lead_times]

            content = "前方英雄【%s 编号:%s】即将在【%s】过期，请及时充能！！" % (
                name, str(obj.id), expire_time.strftime("%Y-%m-%d")
            )

            for lead_time in lead_times:
                date = expire_time - lead_time

                BaseSms.send(self,
                             [u.mobile for u in Group.get_users(DEFAULT_GROUP.SMS.ALERT)],
                             content, date=date, _id="_".join([_id, str(lead_time.days)]))

                BaseMail.send(self,
                              [app.config["MAIL_ALERT"]],
                              content,
                              "",
                              "mail.alert.tpl.html",
                              date=date,
                              _id="_".join([_id, str(lead_time.days)]))

        except Exception, e:
            traceback.print_exc()
            log.exception(e)
            raise ExceptionEx("添加邮件或短信提示失败！")

    def delete_all(self, objs, lead_times):
        for obj in objs:
            self.delete(obj, lead_times)

    def delete(self, obj, lead_times):
        try:
            for lead_time in lead_times:
                try:
                    _id = "_".join([obj.__class__.__name__, str(obj.id), str(lead_time.days)])
                    BaseSms.remove(self, _id)
                    BaseMail.remove(self, _id)
                except JobLookupError, e:
                    traceback.print_exc()
                    log.exception(e)
                    continue

        except Exception, e:
            traceback.print_exc()
            log.exception(e)
            raise ExceptionEx("删除邮件或短信提示失败！")


if __name__ == "__main__":
    from datetime import datetime
    print BaseMail().send(app.config["MAIL_ALERT"],"xxxx","","mail.alert.tpl.html",date=datetime.now(),_id="xawdg")
