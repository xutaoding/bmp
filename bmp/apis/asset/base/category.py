# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import Category


class CategoryApi(BaseApi):
    route = ["/asset/base/category", "/asset/base/category/<int:id>"]

    def get(self, id=0):
        return self.succ(Category.select(id))

    def post(self):
        submit = self.request()
        if not Category.add(submit):
            return self.fail()
        return self.succ()

    def delete(self, id):
        Category.delete(id)
        return self.succ()

    def put(self, id):
        submit = self.request()
        if not Category.edit(id, submit):
            return self.fail()
        return self.succ()


if __name__ == "__main__":
    pass
