# coding: utf-8

from datetime import timedelta

from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import Cert
from bmp.tasks.alert import Alert


class CertApi(BaseApi):
    route = ["/cert", "/cert/<int:id>"]

    def get(self, id=0):
        if id: self.succ(Cert.get(id))
        return self.succ(Cert.select())

    def post(self):
        submit = self.request()
        cert = Cert.add(submit, auto_commit=False)
        Alert().add("证书", cert, cert.end_time, timedelta(days=20))

        db.session.commit()
        return self.succ()

    def delete(self):
        submit = self.request()
        cert = Cert.delete(submit["ids"].split(","), auto_commit=False)
        Alert().delete(cert, timedelta(days=20))

        db.session.commit()
        return self.succ()

    def put(self):
        submit = self.request()
        cert = Cert.edit(submit, auto_commit=False)
        Alert().add("证书", cert, cert.end_time, timedelta(days=20))

        db.session.commit()
        return self.succ()


if __name__ == "__main__":
    c = Cert.get(16)

    r = Cert.edit(c, auto_commit=False)
    print r
