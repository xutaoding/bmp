from bmp import db
from bmp.apis.base import BaseApi


class CategoryApi(BaseApi):
    route=["/asset/base/category"]
    def get(self):
        pass