# coding=utf-8
from bmp import db
from bmp.models.base import BaseModel
from bmp.database import Database
from datetime import datetime
from bmp.utils.exception import ExceptionEx
from bmp.utils.ssh import Client
import json
from bmp import app
import traceback
from sqlalchemy import or_
from bmp import log


class Idc_host_disk(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    device = db.Column(db.Text)
    mount = db.Column(db.Text)
    size_available = db.Column(db.Text)
    size_total = db.Column(db.Text)

    idc_host_id = db.Column(db.Integer, db.ForeignKey("idc_host.id"))


class Idc_host_interface(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    mac_address = db.Column(db.Text)
    interface_name = db.Column(db.Text)
    ip_address = db.Column(db.Text)
    ip_address_mask = db.Column(db.Text)
    ip_address_mt = db.Column(db.Text)

    idc_host_id = db.Column(db.Integer, db.ForeignKey("idc_host.id"))


class Idc_host_ps(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpu_usage = db.Column(db.Text)
    cmd = db.Column(db.Text)
    pid = db.Column(db.Text)
    mem_usage = db.Column(db.Text)
    user = db.Column(db.Text)
    ports = db.Column(db.Text)

    idc_host_id = db.Column(db.Integer, db.ForeignKey("idc_host.id"))

    def __init__(self, submit):
        submit["ports"] = ",".join(submit["ports"])
        BaseModel.__init__(self, submit)

    @classmethod
    def add(cls, iid):
        idc_host = Idc_host.query.filter(Idc_host.id == iid).one()

        client = Client(app.config["SSH_HOST"], app.config["SSH_USER"], app.config["SSH_PASSWORD"])

        def exec_script(path):
            info = client.exec_script(path, idc_host.ip, False)
            return json.loads(info.replace("u'", "'").replace("'", "\""))

        idc_host.ps_info = [Database.to_cls(Idc_host_ps, _dict) for _dict in
                            exec_script("/root/csfscript/host_info/get_ps_info.py")]

        Idc_host_ps.query.filter(Idc_host_ps.idc_host_id == None).delete()

        db.session.commit()
        return True


class Idc_host(BaseModel, db.Model):  # 主机信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(128))
    type_id = db.Column(db.Integer, db.ForeignKey("ref.id"))
    desc = db.Column(db.String(256))
    cate = db.Column(db.String(128))

    host_kernel = db.Column(db.Text)
    cpu_processor = db.Column(db.Text)
    default_gateway = db.Column(db.Text)
    time_zone = db.Column(db.Text)
    processor_cores = db.Column(db.Text)
    product_name = db.Column(db.Text)
    host_lang = db.Column(db.Text)
    memory_total = db.Column(db.Text)
    dns = db.Column(db.Text)
    serial_number = db.Column(db.Text)
    host_interfaces = db.relationship("Idc_host_interface")
    host_disks = db.relationship("Idc_host_disk")
    host_os = db.Column(db.Text)
    processor_vcpus = db.Column(db.Text)
    host_name = db.Column(db.Text)
    ssh_info = db.Column(db.Text)
    system_time = db.Column(db.DateTime)
    ps_info = db.relationship("Idc_host_ps")

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["host_interfaces"] = [i.to_dict() for i in self.host_interfaces]
        _dict["host_disks"] = [d.to_dict() for d in self.host_disks]
        _dict["ps_info"] = [ps.to_dict() for ps in self.ps_info]
        return _dict

    @staticmethod
    def __update(submit):
        client = Client(app.config["SSH_HOST"], app.config["SSH_USER"], app.config["SSH_PASSWORD"])

        def exec_script(path):
            info = client.exec_script(path, submit["ip"], False)
            return json.loads(info.replace("u'", "'").replace("'", "\""))

        if not submit.__contains__("ip"):  # 更新描述信息
            idc_host = Database.to_cls(Idc_host, submit)
            return idc_host

        submit["ssh_info"] = exec_script("/root/csfscript/host_info/get_ssh_info.py")["host_ssh_info"]
        submit["system_time"] = datetime.strptime(
            exec_script("/root/csfscript/host_info/get_system_time.py")["system_time"],
            "%Y-%m-%d %I:%M:%S %p"
        )
        submit.update(exec_script("/root/csfscript/host_info/get_host_info.py"))

        host_interfaces = submit.pop("host_interfaces")
        host_disks = submit.pop("host_disks")

        idc_host = Database.to_cls(Idc_host, submit)
        idc_host.ps_info = [Database.to_cls(Idc_host_ps, _dict) for _dict in
                            exec_script("/root/csfscript/host_info/get_ps_info.py")]

        Idc_host_ps.query.filter(Idc_host_ps.idc_host_id == None).delete()

        idc_host.host_interfaces = [Database.to_cls(Idc_host_interface, _dict) for _dict in host_interfaces]
        idc_host.host_disks = [Database.to_cls(Idc_host_disk, _dict) for _dict in host_disks]
        return idc_host

    @classmethod
    def edit(cls, submit):
        idc_host = Idc_host.__update(submit)
        db.session.commit()
        return True

    @classmethod
    def add(cls, submits):
        results = []
        if not isinstance(submits, list):
            submits = [submits]

        for submit in submits:
            try:
                result = {"ip": submit["ip"], "type_id": submit["type_id"], "success": False, "error": ""}
                results.append(result)

                if Idc_host.query \
                        .filter(Idc_host.ip == submit["ip"]) \
                        .filter(Idc_host.type_id == submit["type_id"]) \
                        .count():
                    result["error"] = "%s 已经存在" % submit["ip"]
                    continue

                idc_host = Idc_host.__update(submit)

                db.session.add(idc_host)

                result["success"] = True
            except  Exception, e:
                log.exception(e)

        db.session.commit()
        return results


if __name__ == "__main__":
    from bmp.models.ref import Ref

    print Idc_host.add({"ip": "192.168.0.231", "type_id": 2})
