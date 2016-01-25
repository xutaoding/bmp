# coding=utf-8
import pyexcel.ext.xlsx
from flask.ext import excel

from bmp.apis.base import BaseApi
import bmp.utils.user_ldap as user_ldap



class Export_usersApi(BaseApi):
    route = ["/users/export"]

    def get(self):

        result=[]
        for u in user_ldap.export(["cn","businessCategory","title","mail"]):
            _dict={
                "名":u["cn"],
                "部门":u["businessCategory"],
                "职务":u["title"],
                "电子邮件地址":u["mail"]
            }
            result.append(_dict)

        resp = excel.make_response_from_records(result, "xlsx")
        resp.headers["Content-Disposition"] = "attachment; filename=user.xlsx"

        return resp
