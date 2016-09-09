# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.doc import Doc


class Doc_export(BaseApi):
    route = ["/doc/export/<string:style>"]

    def get(self, style):
        pass



