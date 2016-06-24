# coding: utf-8
from bmp import db
from bmp.apis.base import BaseApi
from bmp.models.asset import Category


class CategoryApi(BaseApi):
    route = ["/asset/base/category", "/asset/base/category/<int:id>"]

    def get(self, id=0):
        return self.succ(Category.select_sub(id))

    def post(self):
        submit = self.request()
        Category.add(submit)
        return self.succ()

    def delete(self, id):
        Category.delete(id, auto_commit=False)

        db.session.commit()
        return self.succ()

    def put(self, id):
        submit = self.request()
        submit["id"] = id

        Category.edit(submit)
        return self.succ()


if __name__ == "__main__":
    Category.delete(93,auto_commit=False)

    db.session.commit()