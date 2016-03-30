# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Contract
from bmp.tasks.mail.asset.contract import Mail

#todo 短信报警
class ContractApi(BaseApi):
    route = ["/contract", "/contract/<int:id>"]

    def get(self, id=0):
        if id:
            return self.succ(Contract.get(id))
        return self.succ(Contract.select(_orders=[Contract.id.desc()]))

    def post(self):
        submit = self.request()
        contract = Contract.add(submit)
        Mail().to(contract)
        return self.succ()

    def delete(self, id):
        Contract.delete(id)
        return self.succ()

    def put(self, id):
        submit = self.request()
        submit["id"] = id

        Contract.edit(submit)
        return self.succ()


if __name__ == "__main__":
    print Contract.select()
