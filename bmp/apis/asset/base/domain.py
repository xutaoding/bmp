# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Domain
from bmp.tasks.alert import Alert
from datetime import timedelta
from bmp.utils.exception import ExceptionEx
from bmp import db


class DomainApi(BaseApi):
    route = ["/domain", "/domain/<int:id>"]

    def get(self, id=0):
        if id: self.succ(Domain.get(id))
        return self.succ(Domain.select(_orders=Domain.end_time))

    def post(self):
        submit = self.request()
        domain = Domain.add(submit,auto_commit=False)
        Alert().add("域名", domain, domain.end_time, timedelta(days=30))

        db.session.commit()
        return self.succ()

    def delete(self):
        submit = self.request()

        if len(submit["ids"].split(",")) > 1:
            raise ExceptionEx("批量操作暂时无法使用")

        domain = Domain.delete(submit["ids"].split(","),auto_commit=False)
        Alert().delete(domain,[timedelta(30), timedelta(60)])

        db.session.commit()
        return self.succ()

    def put(self):
        submit = self.request()

        if len(submit) > 1:
            raise ExceptionEx("批量操作暂时无法使用")

        domain = Domain.edit(submit,auto_commit=False)
        Alert().add("域名", domain, domain.end_time, timedelta(days=30))

        db.session.commit()
        return self.succ()


if __name__ == "__main__":
    pass
