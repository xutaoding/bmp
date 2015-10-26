#coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.purchase import Purchase,PurchaseApproval,PurchaseGoods,PurchaseImg
from bmp.models.asset import Supplier,Contract
from bmp.models.user import Group
from flask import session
from bmp.const import USER_SESSION,PURCHASE

class PurchaseApi(BaseApi):
    route=["/purchase","/purchase/<int:pid>","/purchase/<int:page>/<int:pre_page>"]

    def auth(self):
        session[USER_SESSION]={"uid":"jim.zhao"}
        return True

    def get(self,page=0,pre_page=0):
        g_dict={}
        for g in set(PURCHASE.FLOW).difference([PURCHASE.FLOW_ONE]):
            g_dict[g]=[user.uid for user in Group.get_users(g)]

        page=Purchase.unfinished(g_dict,page,pre_page)
        return self.succ(page)

    def put(self,pid):
        submit=self.request()
        PurchaseApproval.edit(pid,submit)
        return self.succ()

    def post(self):
        submit=self.request()
        submit["supplier"]=Supplier.get(submit["supplier_id"])
        submit["contract"]=Contract(submit["contract"])
        submit["approvals"]=[]
        Purchase.add(submit)
        return self.succ()

    def delete(self,pid):
        Purchase.delete(pid)
        return self.succ()

if __name__=="__main__":
    from bmp.utils.post import test

    test("post",
         "http://192.168.0.143:5000/apis/v1.0/purchase",
         {
             "contract":{
                 "begin_time":"2015-01-01 01:01:01",
                 "end_time":"2015-01-02 01:01:01",
                 "path":"合同文件路径"
             },
             "imgs":[{
                     "b64":"图片编码内容",
                     "desc":"描述"
             }],
             "goods":[{
                 "name":"商品名称",
                 "price":"11.11",
                 "spec":"规格",
                 "amount":"10"
             }],
             "supplier_id":1,#供应商id
             "use":"用途"
         },True)




