# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Domain


class DomainApi(BaseApi):
    route = ["/domain", "/domain/<int:id>"]

    def get(self, id=0):
        if id:self.succ(Domain.get(id))
        return self.succ(Domain.select())

    def post(self):
        submit = self.request()
        Domain.add(submit)
        return self.succ()

    def delete(self, id):
        Domain.delete(id)
        return self.succ()

    def put(self):
        submit=self.request()
        Domain.edit(submit)
        return self.succ()


if __name__ == "__main__":
    pass
