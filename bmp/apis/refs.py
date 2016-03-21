# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.ref import Ref


class RefsApi(BaseApi):
    route = ["/refs", "/refs/<string:type>"]

    def get(self, type="%"):
        return self.succ(Ref.select(type))

    def post(self):
        submit = self.request()
        Ref.add(submit["name"], submit["type"], submit["parent_id"])
        return self.succ()

    def delete(self, id):
        Ref.delete(id)
        return self.succ()




if __name__=="__main__":
    Ref.add("chinascopefinancial.com","web",0)
    Ref.add("CAM","web",0)
    Ref.add("OMS","web",0)
    Ref.add("智投H5活动页面","web",0)
    Ref.add("ichinascope","web",0)
    Ref.add("数库港","web",0)
    Ref.add("智投WEB版","web",0)
    Ref.add("智投admin后台","web",0)
    Ref.add("nlp-csf","web",0)
    Ref.add("基金","web",0)
    Ref.add("developer接口","web",0)
    Ref.add("量化","web",0)
    Ref.add("整合账户系统","web",0)
    Ref.add("数库指数","web",0)
