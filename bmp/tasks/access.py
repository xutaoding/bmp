import json

from bmp import app
from bmp.utils.ssh import Client


class DeploySsh:
    def __init__(self,timeout=3):
        self.client = Client(app.config["SSH_HOST"], app.config["SSH_USER"], app.config["SSH_PASSWORD"])
        self.timeout = timeout

    def add(self, content):
        ret = self.client.exec_script("/root/csfscript/server_ssh/add_auth.py", content,timeout=self.timeout)
        return ret

    def delete(self, content):
        ret = self.client.exec_script("/root/csfscript/server_ssh/del_auth.py", content)
        return True if "ok" in ret else False

    def list(self, content):
        ret = self.client.exec_script("/root/csfscript/server_ssh/list_auth.py", content)
        return json.loads(ret)
