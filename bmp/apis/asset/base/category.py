from bmp import db
from bmp.apis.base import BaseApi


class CategoryApi(BaseApi):
    route = ["/asset/base/category/devicetype/<int:id>", "/asset/base/category/devicename/<int:id>",
             "/asset/base/category/elaborate/<int:id>"]
    # route=["/asset/base/category"]

    def auth(self):
        return True

    def get(self, id=0):pass
        #return self.succ(DeviceType.history())

    def post_devicetype(self):
        submit = self.request()

        return self.succ()

    def post_devicename(self):
        submit = self.request()
        #DeviceName.add(submit)
        return self.succ()

    def post_elaborate(self):
        submit = self.request()
        #Elaborate.add(submit)
        return self.succ()

    def delete_devicetype(self, id):
        #DeviceType.delete(id)
        #DeviceName.delete()
        return self.succ()

    def delete_devicename(self, id):
        #DeviceName.delete(id)
        return self.succ()

    def delete_elaborate(self, id):
        #Elaborate.delete(id)
        return self.succ()




