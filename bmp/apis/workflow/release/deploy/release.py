# coding=utf-8
from bmp.apis.base import BaseApi
from bmp.models.release import Release

from bmp.tasks.release import deploy_database


class ReleaseApi(BaseApi):
    route = ["/release/deploy/<int:rid>", "/release/deploy/<int:page>/<int:pre_page>"]

    def get(self, page, pre_page):
        return self.succ(Release.undeployed(page, pre_page))

    def post(self, rid):
        deploy_database(rid)
        return self.succ()

    def put(self, rid):
        Release.deploy(rid)
        return self.succ()


if __name__ == "__main__":
    from bmp.utils.ssh import Client

    client = Client("192.168.250.253", "depops", password="Passwd@!")

    data = {
        "dbs": [
            {
                "dbtype": "mongodb",
                "dbname": "test",
                "tables": ["testData1", "testData2"]
            }
        ],
        "s_host": "192.168.250.253",
        "d_host": ["192.168.250.111"]
    }

    data = {}
    data["dbs"] = []
    r = Release.get(129)

    dbtype = r["service"]["type"]
    for db in r["service"]["databases"]:
        dbs = {"dbtype": dbtype}
        dbs["dbname"] = db["name"]
        dbs["tables"] = [t["name"] for t in db["tables"] if t["name"] != "[ALL]"]
        data["dbs"].append(dbs)

    fmt_host = lambda x: x.split("——")[1]

    data["s_host"] = fmt_host(r["_from"])
    data["d_host"] = fmt_host(r["to"])

    client = Client("192.168.0.227", "root", rsakey="C:\Users\chenglong.yan\.ssh\id_rsa")
    client.exec_script("/root/csfscript/dump_data/dump_data.py", data)

"""
/var/www/scope/bmp/bmp/data_deploy_log/
脚本成功返回：任务完成
    失败返回：任务失败
"""

# print client.exec_command("ls /root/csfscript/dump_data/logs")
# print client.exec_command("sudo  /root/csfscript/dump_data/dump_data.py \"%s\""%json.dumps(data).replace("\"","\\\""))
