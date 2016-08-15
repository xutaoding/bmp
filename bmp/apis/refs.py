# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.ref import Ref


class RefsApi(BaseApi):
    route = ["/refs", "/refs/<string:type>", "/refs/<int:rid>"]

    def get(self, type="%"):
        return self.succ(Ref.select(type))

    def post(self):
        submit = self.request()
        Ref.add(submit["name"], submit["type"], submit["parent_id"])
        return self.succ()

    def delete(self, rid):
        Ref.delete(rid)
        return self.succ()


if __name__ == "__main__":
    pass
