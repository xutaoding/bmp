# coding: utf-8

import bmp.utils.sms as sms
from bmp.tasks.base import BaseTask


class BaseSms(BaseTask):
    def send(self, mobiles, content, date=None, _id=None):
        for mobile in mobiles:
            self.add_job(sms.send, args=(mobile, content), date=date, _id="_".join(["sms", _id]))

    def remove(self,_id):
        _id="_".join(["sms", _id])
        self.remove_job(_id)


if __name__ == "__main__":
    pass

