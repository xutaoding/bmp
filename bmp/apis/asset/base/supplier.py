# coding: utf-8
from flask import session
from bmp.const import USER_SESSION
from bmp.apis.base import BaseApi
from bmp.models.supplier import Supplier
import json

class SupplierApi(BaseApi):
    route = ["/supplier", "/supplier/<int:id>"]
    # route = "/supplier"
    def auth(self):
        return True

    # 页面上是get请求？！，可以传参（参考）
    def get(self, id=1):
        return self.succ(Supplier.get(id))

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


    test(
        "post",
        "http://192.168.0.57:5000/apis/v1.0/supplier",
        {
            "name":"惠普",
            "connector":"dgsg",
            "mobile":"43564765",
            "address":"上海市",
            "interfaceor":"上海数库"

        },True
    )



    # test(
    #     "delete",
    #     "http://192.168.0.57:5000/apis/v1.0/supplier/1",
    #     {
    #         "id":1,
    #         "name":"惠普",
    #         "connector":"dgsg",
    #         "mobile":"43564765",
    #         "address":"上海市",
    #         "interfaceor":"上海数库"
    #     },True
    # )

    # test(
    #     "put",
    #     "http://192.168.0.57:5000/apis/v1.0/supplier/1",
    #     {
    #         "id":1,
    #         "name":"联想",
    #         "connector":"dgsg",
    #         "mobile":"43564765",
    #         "address":"上海市",
    #         "interfaceor":"北京数库"
    #     },True
    # )

