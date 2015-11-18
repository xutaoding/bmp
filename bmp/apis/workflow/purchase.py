# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.purchase import Purchase, PurchaseApproval
from bmp.models.asset import Supplier, Contract
from bmp.models.user import Group
from flask import session
from bmp.const import USER_SESSION, PURCHASE
from bmp.database import Database
from bmp.utils.exception import ExceptionEx

from flask.ext import excel


class PurchaseApi(BaseApi):
    route = ["/purchase", "/purchase/<int:pid>", "/purchase/<int:page>/<int:pre_page>"]

    def approval(self, pid):
        Purchase.approval(pid)
        return self.succ()

    def saved(self, page=0, pre_page=None, pid=0):
        if pid:
            return self.succ(Purchase.get(pid))
        page = Purchase.drafts(page, pre_page)
        return self.succ(page)

    def get(self, pid=0):
        if pid:
            return self.succ(Purchase.get(pid))
        g_dict = {}
        for g in set(PURCHASE.FLOW).difference([PURCHASE.FLOW_ONE]):
            g_dict[g] = [user.uid for user in Group.get_users(g)]
        unfinished = Purchase.unfinished(g_dict)
        return self.succ(unfinished)

    def passed(self,page=0,pre_page=None):
        return self.succ(Purchase.passed(page,pre_page))


    def __submit(self):
        submit = self.request()

        if not submit.__contains__("supplier_id"):
            raise ExceptionEx("供应商不能为空")

        submit["supplier"] = Supplier.query.filter(Supplier.id == submit["supplier_id"]).one()
        if submit.__contains__("contract"):
            submit["contract"] = Database.to_cls(Contract, submit["contract"])
        else:
            submit["contract"] = None
        return submit

    def save(self):
        submit = self.__submit()
        Purchase.edit(submit)
        return self.succ()

    def put(self, pid):
        submit = self.request()
        PurchaseApproval.edit(pid, submit)
        return self.succ()

    def post(self):
        submit = self.__submit()
        Purchase.add(submit)
        return self.succ()

    def delete(self, pid):
        Purchase.delete(pid)
        return self.succ()

    def search(self, page=None, pre_page=None):
        submit = self.request()
        return self.succ(Purchase.search(submit, page, pre_page))

if __name__ == "__main__":
    from bmp.utils.post import test

    result = test("search",
                  "http://localhost:5000/apis/v1.0/purchase",
                  {
                      "goods": "3333",
                      "price": "2222"
                  }, True)

    with open("test.csv", "w") as t: t.write(result)

    test("GET",
         "http://192.168.0.143:5000/apis/v1.0/purchase/1",
         {
             "id": "1",
             "contract": {
                 "id": "2",
                 "begin_time": "2015-01-01 01:01",
                 "end_time": "2015-01-02 01:01",
                 "path": "合同文件路径2"
             },
             "imgs": [{
                 "id": "2",
                 "b64": "图片编码内容2",
                 "desc": "描述2"
             }],
             "goods": [{
                 "id": "2",
                 "name": "商品名称2",
                 "price": "11.11",
                 "spec": "规格2",
                 "amount": "10"
             }],
             "supplier_id": 1,  # 供应商id
             "use": "用途2"
         })