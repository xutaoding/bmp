#coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.purchase import Purchase,PurchaseApproval,PurchaseGoods,PurchaseImg
from bmp.models.asset import Supplier,Contract


class PurchaseApi(BaseApi):
    route=["/purchase","/purchase/<int:pid>","/purchase/<int:page>/<int:pre_page>"]

    def get(self,page,pre_page):
        return self.succ(Purchase.page(page,pre_page))

    def post(self):
        submit=self.request()
        Purchase.add(submit)
        return self.succ()

    def delete(self):
        return self.succ()

if __name__=="__main__":
    from bmp.utils.post import test

    test("post",
         "http://192.168.0.143:5000/apis/v1.0/purchase",
         {
             "approvals":[],
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
             "supplier_id":1,
             "use":"用途"
         })




