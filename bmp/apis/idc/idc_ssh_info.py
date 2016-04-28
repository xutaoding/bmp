# coding: utf-8
import json

from bmp import app
from bmp.apis.base import BaseApi
from bmp.utils.ssh import Client


class Idc_ssh_infoApi(BaseApi):
    route = ["/idc/ssh/<string:ip>"]

    def get(self, ip):
        client = Client(app.config["SSH_IDC_HOST"], app.config["SSH_IDC_USER"], app.config["SSH_IDC_PASSWORD"])

        def exec_script(path):
            info = client.exec_script(path, ip, False)
            return json.loads(info.replace("u'", "'").replace("'", "\""))

        return self.succ(
            exec_script("/root/csfscript/host_info/get_ssh_info.py")["host_ssh_info"].replace("\n", "&#10;").replace(
                " ", "&#160;"))


if __name__ == "__main__":
    client = Client(app.config["SSH_IDC_HOST"], app.config["SSH_IDC_USER"], app.config["SSH_IDC_PASSWORD"])


    def exec_script(path):
        info = client.exec_script(path, "192.168.0.231", False)
        return json.loads(info.replace("u'", "'").replace("'", "\""))


    exec_script("/root/csfscript/host_info/get_ssh_info.py")["host_ssh_info"].split("\n")
