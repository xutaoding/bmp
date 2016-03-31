# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Contract
from bmp.tasks.alert import Alert
from datetime import timedelta
from bmp import db


class ContractApi(BaseApi):
    route = ["/contract", "/contract/<int:id>"]

    def get(self, id=0):
        if id:
            return self.succ(Contract.get(id))
        return self.succ(Contract.select(_orders=[Contract.id.desc()]))

    def post(self):
        submit = self.request()
        contract = Contract.add(submit, auto_commit=False)
        Alert().add("合同", contract, contract.end_time, [timedelta(30), timedelta(60)])

        db.session.commit()
        return self.succ()

    def delete(self, id):
        contract = Contract.delete(id,auto_commit=False)
        Alert().delete(contract,[timedelta(30), timedelta(60)])

        db.session.commit()
        return self.succ()

    def put(self, id):
        submit = self.request()
        submit["id"] = id
        contract = Contract.edit(submit,auto_commit=False)
        Alert().add("合同", contract, contract.end_time, [timedelta(30), timedelta(60)])

        db.session.commit()
        return self.succ()


if __name__ == "__main__":
    print Contract.select()
