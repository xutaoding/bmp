# coding: utf-8
from flask import session
from bmp.const import USER_SESSION
from bmp.apis.base import BaseApi
from bmp.models.asset import Supplier
import json

class SupplierApi(BaseApi):
    route = ["/supplier", "/supplier/<int:id>"]
    # route = "/supplier"
    def auth(self):
        return True

    # 页面上是get请求？！，可以传参（参考）
    def get(self, id=0):
        return self.succ(Supplier.history())

    def post(self):
        submit = self.request()
        Supplier.add(submit)
        return self.succ()

    def delete(self,id):
        Supplier.delete(id)
        return self.succ()

    def put(self,id):
        submit = self.request()
        Supplier.edit(id, submit)
        return self.succ()





if __name__ == "__main__":
    from bmp.utils.post import test


    # test(
    #     "post",
    #     "http://192.168.0.57:5000/apis/v1.0/supplier",
    #     {
    #         "name":"联想",
    #         "connector":"dgsg",
    #         "tel":"43564765",
    #         "addr":"上海市",
    #         "interfaceor":"上海数库"
    #
    #     },True
    # )



    # test(
    #     "delete",
    #     "http://192.168.0.57:5000/apis/v1.0/supplier/2",
    #     {
    #         "name":"lian",
    #         "connector":"dgsg",
    #         "tel":"43564765",
    #         "addr":"上海市",
    #         "interfaceor":"上海数库"
    #     },
    #     True
    # )

    # test(
    #     "put",
    #     "http://192.168.0.57:5000/apis/v1.0/supplier/1",
    #     {
    #         "id":1,
    #         "name":"联想",
    #         "connector":"dgsg",
    #         "tel":"43564765",
    #         "addr":"上海市",
    #         "interfaceor":"北京数库"
    #     },True
    # )

