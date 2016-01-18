# coding=utf-8
from bmp.models.release import Release
from bmp.utils.ssh import Client
from bmp import app, db

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
    "mysqldb-01.csilcsoh66yg.rds.cn-north-1.amazonaws.com.cn": "54.223.37.5"
}


def fmt_host(_from, to):
    s_host = _from.split("——")[1]
    d_host = to.split("——")[1]

    if ip_dict.__contains__(d_host):
        d_host = ip_dict[d_host]

    return s_host, d_host


def deploy_database(rid):
    r = Release.query.filter(Release.id == rid).one()

    data = {}
    data["dbs"] = []

    dbtype = r.service.type
    for d in r.service.databases:
        dbs = {"dbtype": dbtype}
        dbs["dbname"] = d.name
        dbs["tables"] = [t.name for t in d.tables if t.name != "[ALL]"]
        data["dbs"].append(dbs)

    data["s_host"], data["d_host"] = fmt_host(r._from, r.to)

    client = Client(app.config["SSH_HOST"], app.config["SSH_USER"], app.config["SSH_PASSWORD"])

    result = {"params": data}
    result["return"] = client.exec_script("/root/csfscript/dump_data/dump_data.py", data)

    if u"任务失败" in result["return"]:
        return result

    r.is_deployed = True
    db.session.commit()
    return result


if __name__ == "__main__":
    pass
