# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.purchase import Purchase, PurchaseApproval
from bmp.models.asset import Supplier, Contract
from bmp.models.user import Group
from bmp.const import PURCHASE
from bmp.database import Database
from bmp.utils.exception import ExceptionEx
from bmp.tasks.mail.purchase import Mail


class PurchaseApi(BaseApi):
    route = ["/purchase", "/purchase/<int:pid>", "/purchase/<int:page>/<int:pre_page>"]

    def approval(self, pid):
        Purchase.approval(pid)
        Mail().to(Purchase.query.filter(Purchase.id == pid).one())
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

    def finished(self, page=0, pre_page=None):
        return self.succ(Purchase.finished(page, pre_page))

    def passed(self, page=0, pre_page=None):
        return self.succ(Purchase.passed(page, pre_page))

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
        Mail().to(Purchase.query.filter(Purchase.id == pid).one())
        return self.succ()

    def post(self):
        submit = self.__submit()
        purchase = Purchase.add(submit)
        return self.succ()

    def delete(self, pid):
        Purchase.delete(pid)
        return self.succ()

    def search(self, page=None, pre_page=None):
        submit = self.request()
        return self.succ(Purchase.search(submit, page, pre_page))


if __name__ == "__main__":
    Purchase.delete(94)
