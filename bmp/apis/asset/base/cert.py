# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Cert
from bmp.tasks.mail.asset.cert import Mail

#todo 短信报警
class CertApi(BaseApi):
    route = ["/cert", "/cert/<int:id>"]

    def get(self, id=0):
        if id: self.succ(Cert.get(id))
        return self.succ(Cert.select())

    def post(self):
        submit = self.request()
        cert = Cert.add(submit)
        Mail().to(cert)
        return self.succ()

    def delete(self):
        submit = self.request()
        Cert.delete(submit["ids"].split(","))
        return self.succ()

    def put(self):
        submit = self.request()

        certs = Cert.edit(submit)
        mail = Mail()

        for cert in certs: mail.to(cert)
        return self.succ()


if __name__ == "__main__":
    pass
