#coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.purchase import Purchase,PurchaseApproval
from bmp.models.asset import Supplier,Contract
from bmp.models.user import Group
from flask import session
from bmp.const import USER_SESSION,PURCHASE
from bmp.database import Database

class PurchaseApi(BaseApi):
    route=["/purchase","/purchase/<int:pid>","/purchase/<int:page>/<int:pre_page>/<int:is_draft>"]
    methods =["approval","saved"]

    def auth(self):
        session[USER_SESSION]={"uid":"chenglong.yan","businessCategory":"it"}
        return True

    def approval(self,pid):
        Purchase.approval(pid)
        return self.succ()

    def saved(self,page=0,pre_page=None):
        page=Purchase.drafts(page,pre_page)
        return self.succ(page)

    def get(self,page=0,pre_page=None):
        if not pre_page:
            return self.succ(Purchase.get(page))
        g_dict={}
        for g in set(PURCHASE.FLOW).difference([PURCHASE.FLOW_ONE]):
            g_dict[g]=[user.uid for user in Group.get_users(g)]
        page=Purchase.unfinished(g_dict,page,pre_page)
        return self.succ(page)

    def __submit(self):
        submit=self.request()
        submit["supplier"]=Supplier.get(submit["supplier_id"])
        if submit["contract"]:
            submit["contract"]=Database.to_cls(Contract,submit["contract"])
        else:
            submit["contract"]=None
        return submit

    def save(self):
        submit=self.__submit()
        Purchase.edit(submit)
        return self.succ()

    def put(self,pid):
        submit=self.request()
        PurchaseApproval.edit(pid,submit)
        return self.succ()

    def post(self):
        submit=self.__submit()
        Purchase.add(submit)
        return self.succ()

    def delete(self,pid):
        Purchase.delete(pid)
        return self.succ()

if __name__=="__main__":
    from bmp.utils.post import test

    test("approval",
         "http://192.168.0.143:5000/apis/v1.0/purchase",
         {
             "id":"1",
             "contract":{
                 "id":"2",
                 "begin_time":"2015-01-01 01:01",
                 "end_time":"2015-01-02 01:01",
                 "path":"合同文件路径2"
             },
             "imgs":[{
                    "id":"2",
                     "b64":"图片编码内容2",
                     "desc":"描述2"
             }],
             "goods":[{
                 "id":"2",
                 "name":"商品名称2",
                 "price":"11.11",
                 "spec":"规格2",
                 "amount":"10"
             }],
             "supplier_id":1,#供应商id
             "use":"用途2"
         },True)




