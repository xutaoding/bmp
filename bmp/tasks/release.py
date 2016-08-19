# coding=utf-8
import threading
from datetime import datetime

from bmp import app, db, log
from bmp.models.release import Release
from bmp.utils.ssh import Client

"""
122.144.134.3	122.144.134.3
122.144.167.124	122.144.167.124
122.144.134.6	122.144.134.6
54.251.56.179	54.251.56.179
54.223.37.5	    54.223.37.5
122.144.134.3	122.144.134.3
54.251.56.179	sg-com-csf-web-db.cwiif0vzcyt6.ap-southeast-1.rds.amazonaws.com
54.223.37.5     mysqldb-01.csilcsoh66yg.rds.cn-north-1.amazonaws.com.cn
"""

ip_dict = {
    "sg-com-csf-web-db.cwiif0vzcyt6.ap-southeast-1.rds.amazonaws.com": "54.251.56.179",
    "mysqldb-01.csilcsoh66yg.rds.cn-north-1.amazonaws.com.cn": "54.223.37.5",
    "122.144.134.3": "192.168.251.3",
    "122.144.134.6": "192.168.251.6",
    "122.144.134.95": "192.168.251.95",
    "122.144.134.21": "192.168.251.21",
    "122.144.134.5": "192.168.251.5"
}


def fmt_host(_from, to):
    d_hosts = []
    s_host = _from.split("——")[1]

    for _to in to.split(" "):
        if not _to: continue
        d_host = _to.split("——")[1]
        if ip_dict.__contains__(d_host):
            d_host = ip_dict[d_host]
        d_hosts.append(d_host)

    return s_host, d_hosts


def __deploy_database(rid, data):
    r = Release.query.filter(Release.id == rid).one()
    try:

        client = Client(app.config["SSH_HOST"], app.config["SSH_USER"], app.config["SSH_PASSWORD"])

        if u"任务完成" not in client.exec_script("/root/csfscript/dump_data/dump_data.py", data):
            return

        r.is_deployed = True

        log_path = "%s/data_deploy_log/myapp.%s" % (app.root_path, datetime.now().strftime("%Y-%m-%d"))
        Release.add_log(r.id, log_path)
    except Exception, e:
        log.exception(e)
    finally:
        r.is_deploying = False
        r.deploy_times += 1
        db.session.commit()


def deploy_database(rid):
    r = Release.query.filter(Release.id == rid).one()
    r.deploy_time = datetime.now()
    r.is_deploying = True

    dbtype = r.service.type
    data = {"dbs": []}
    for d in r.service.databases:
        dbs = {"dbtype": dbtype}
        dbs["dbname"] = d.name
        dbs["tables"] = [t.name for t in d.tables if t.name != "[ALL]"]
        data["dbs"].append(dbs)

    data["s_host"], data["d_host"] = fmt_host(r._from, r.to)
    db.session.commit()

    threading.Thread(target=__deploy_database, args=(rid, data,)).start()

    return data


if __name__ == "__main__": pass
# print deploy_database(161)
