# coding: utf-8

import bmp.utils.sms as sms
from bmp.tasks.base import BaseTask


class BaseSms(BaseTask):
    def send(self, mobiles, content, date=None, _id=None):
        for mobile in mobiles:
            self.add_job(sms.send, args=(mobile, content), date=date, _id=_id)


if __name__ == "__main__":
    from datetime import datetime
    BaseSms().send(["15618226618"],"神盾局OPS系统：前方英雄【%s】即将在【%s】过期，请及时充能！！",datetime.now())
