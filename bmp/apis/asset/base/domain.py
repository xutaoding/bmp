# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Domain
from bmp.tasks.mail.asset.domain import Mail


class DomainApi(BaseApi):
    route = ["/domain", "/domain/<int:id>"]

    def get(self, id=0):
        if id:self.succ(Domain.get(id))
        return self.succ(Domain.select())

    def post(self):
        submit = self.request()
        domain=Domain.add(submit)
        Mail().to(domain)
        return self.succ()

    def delete(self):
        submit = self.request()
        Domain.delete(submit["ids"].split(","))
        return self.succ()

    def put(self):
        submit=self.request()

        domains=Domain.edit(submit)

        mail=Mail()
        for domain in domains:
            mail.to(domain)

        return self.succ()


if __name__ == "__main__":
    pass
