# coding=utf-8
from flask.ext import excel

from bmp.apis.base import BaseApi
from bmp.utils.user_ldap import Ldap


class Export_usersApi(BaseApi):
    route = ["/users/export", "/users/export/<string:field>"]

    def get(self, field=""):
        result = []

        field_default = {
            "cn": "名",
            "businessCategory": "部门",
            "title": "职务",
            "mail": "电子邮件地址",
        }

        field_ext = {
            "mobile": "手机"
        }

        fields = dict(field_default.items() + field_ext.items())

        if field in fields.keys():
            fields = {field: fields[field], "uid": "用户名"}
        else:
            fields = field_default

        ldap = Ldap()

        for u in ldap.export(fields.keys()):
            _dict = {}
            for key in u.keys(): _dict[fields[key]] = u[key]
            result.append(_dict)

        resp = excel.make_response_from_records(result, "xlsx")
        resp.headers["Content-Disposition"] = "attachment; filename=user.xlsx"
        return resp
