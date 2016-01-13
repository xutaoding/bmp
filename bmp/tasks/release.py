# coding=utf-8
from bmp.models.release import Release
from bmp.utils.ssh import Client
from bmp import app,db
from bmp.utils.exception import ExceptionEx

def deploy_database(rid):
    r = Release.query.filter(Release.id==rid).one()

    data = {}
    data["dbs"] = []

    dbtype = r.service.type
    for d in r.service.databases:
        dbs = {"dbtype": dbtype}
        dbs["dbname"] = d["name"]
        dbs["tables"] = [t["name"] for t in d["tables"] if t["name"] != "[ALL]"]
        data["dbs"].append(dbs)

    fmt_host = lambda x: x.split("——")[1]

    data["s_host"] = fmt_host(r["_from"])
    data["d_host"] = fmt_host(r["to"])

    client = Client(app.config["SSH_HOST"],app.config["SSH_USER"],app.config["SSH_PASSWORD"])
    if u"任务失败" in client.exec_script("/root/csfscript/dump_data/dump_data.py", data):
        raise ExceptionEx("任务失败")

    r.is_deployed=True
    db.session.commit()
    return True


if __name__ == "__main__":
    pass
