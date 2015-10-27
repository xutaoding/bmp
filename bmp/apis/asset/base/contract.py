# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.supplier import Contract


class ContractApi(BaseApi):
    route = ["/contract", "/contract/<int:id>"]

    def auth(self):
        return True

    def get(self, id=0):
        return self.succ(Contract.get(id))

    # return self.succ()里面均可以为空
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

    # test(
    #     "post",
    #     "http://192.168.0.57:5000/apis/v1.0/contract",
    #     {
    #         "id":1,
    #         "signDate": "2014-02-12",
    #         "stopDate": "2015-08-25",
    #         "buyer": "yara.yu",
    #         "seller": "联想",
    #         "content":"联想电脑采购10台",
    #         "detailed": "其配置为：inter"
    #
    #     }, True
    # )

    # test(
    #     "delete",
    #     "http://192.168.0.57:5000/apis/v1.0/contract/1",
    #     {
    #         "id": 1,
    #         "signDate": "2014-02-12",
    #         "stopDate": "2015-08-25",
    #         "buyer": "yara.yu",
    #         "seller": "联想",
    #         "content":"联想电脑采购10台",
    #         "detailed": "其配置为：inter"
    #     },True
    # )
    #
    # test(
    #     "put",
    #     "http://192.168.0.57:5000/apis/v1.0/contract/1",
    #     {
    #         "id": 1,
    #         "signDate": "2005-09-22",
    #         "stopDate": "2015-08-25",
    #         "buyer": "yara.yu",
    #         "seller": "惠普",
    #         "content":"惠普电脑采购20台",
    #         "detailed": "其配置为：inter"
    #     }, True
    # )
