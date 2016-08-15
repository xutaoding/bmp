# coding: utf-8
import json

from bmp import app
from bmp.apis.base import BaseApi
from bmp.utils.ssh import Client


class Idc_system_timeApi(BaseApi):
    route = ["/idc/time/<string:ip>"]

    def get(self, ip):
        client = Client(app.config["SSH_IDC_HOST"], app.config["SSH_IDC_USER"], app.config["SSH_IDC_PASSWORD"])

        def exec_script(path):
            info = client.exec_script(path, ip, False)
            return json.loads(info.replace("u'", "'").replace("'", "\""))

        return self.succ(exec_script("/root/csfscript/host_info/get_system_time.py")["system_time"])


if __name__ == "__main__":
    pass
