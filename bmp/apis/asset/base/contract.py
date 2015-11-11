# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.asset import Contract


class ContractApi(BaseApi):
    route = ["/contract", "/contract/<int:id>"]

    def get(self, id=0):
        return self.succ(Contract.select())

    def post(self):
        submit = self.request()
        Contract.add(submit)
        return self.succ()

    def delete(self, id):
        Contract.delete(id)
        return self.succ()

    def put(self, id):
        submit = self.request()
        Contract.edit(id, submit)
        return self.succ()


if __name__ == "__main__":
    from bmp.utils.post import test

    test(
        "post",
        "http://192.168.0.57:5000/apis/v1.0/contract",
        {
            "begin_time": "2014-02-12 08:45",
            "end_time": "2015-08-25 11:22",
            "purchase_id": 5,
            "supplier_name": "联想",
            "path": "D:\PythonCode"

        }
    )

    test(
        "delete",
        "http://192.168.0.57:5000/apis/v1.0/contract/1",
        {
            "begin_time": "2014-02-12 08:45",
            "end_time": "2015-08-25 11:22",
            "purchase_id": 4,
            "supplier_name": "联想",
            "path": "D:\PythonCode"
        }
    )

    test(
        "put",
        "http://192.168.0.57:5000/apis/v1.0/contract/1",
        {
            "begin_time": "2014-02-12 05:33",
            "end_time": "2014-08-13 23:00",
            "purchase_id": 4,
            "supplier_name": "联想",
            "path": "D:\PythonCode"
        }
    )
