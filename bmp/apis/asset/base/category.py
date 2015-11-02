# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import Category


class CategoryApi(BaseApi):
    route = ["/asset/base/category/<int:id>"]
    # route=["/asset/base/category"]

    def auth(self):
        return True

    def get(self, parent_id=0):
        return self.succ(Category.history(parent_id))

    def post(self):
        submit = self.request()
        Category.add(submit)
        return self.succ()

    def delete(self, id):
        Category.delete(id)
        return self.succ()


    def put(self, id):
        print 'ss:', id
        submit = self.request()
        Category.edit(id, submit)
        return self.succ()


if __name__ == "__main__":
    from bmp.utils.post import test

    test(
        "delete",
        "http://192.168.0.57:5000/apis/v1.0/asset/base/category/3",
        {
            "id": "3",
            "name": "路由器",
            "parent_id": "2"
        },
        True

    )