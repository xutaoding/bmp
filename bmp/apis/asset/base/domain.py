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
        return self.succ(Domain.add(submit))

    def delete(self, id):
        Domain.delete(id)
        return self.succ()

    def put(self, id):
        submit=self.request()
        submit["id"]=id
        Domain.edit(submit)
        return self.succ()


if __name__ == "__main__":
    Domain.add({
        "name":"baidu.com",
        "sp":"万网",
        "end_time":"2000-01-01"
    })
