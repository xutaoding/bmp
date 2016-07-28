# coding: utf-8
from bmp import db
from bmp.models.base import BaseModel
import json

class DocIndex(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no = db.Column(db.Integer)
    name = db.Column(db.String(128))
    field = db.Column(db.String(128))
    desc = db.Column(db.String(128))
    is_unique = db.Column(db.Boolean)

    doc_id = db.Column(db.Integer, db.ForeignKey("doc.id"))


class DocField(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no = db.Column(db.Integer)
    name = db.Column(db.String(128))
    type = db.Column(db.String(128))
    desc = db.Column(db.String(128))

    doc_id = db.Column(db.Integer, db.ForeignKey("doc.id"))


class DocHistory(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    opt = db.Column(db.String(128))
    type = db.Column(db.String(128))

    content = db.Column(db.Text)
    create_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    create_time = db.Column(db.DateTime)

    doc_id = db.Column(db.Integer, db.ForeignKey("doc.id"))

    def _to_dict(self):
        hist = self.to_dict()
        hist["content"] = json.loads(hist["content"])

        return hist



class Doc(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    database = db.Column(db.String(128))
    table = db.Column(db.String(256))
    env = db.Column(db.String(128))
    pkey = db.Column(db.String(256))
    init_len = db.Column(db.Integer)
    max_len = db.Column(db.Integer)
    desc = db.Column(db.Text)
    example = db.Column(db.Text)

    mainten_uid = db.Column(db.String(128), db.ForeignKey("user.uid"), default=None)
    opt_uid = db.Column(db.String(128), db.ForeignKey("user.uid"), default=None)
    create_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    create_time = db.Column(db.DateTime)

    is_del = db.Column(db.Boolean, default=False)

    historys = db.relationship("DocHistory")
    fields = db.relationship("DocField")
    indexs = db.relationship("DocIndex")

    def _to_dict(self):
        _dict = self.to_dict()
        _dict["indexs"] = [i.to_dict() for i in self.indexs]
        _dict["fields"] = [f.to_dict() for f in self.fields]
        historys = self.historys
        _dict["modify_time"] = historys[-1].to_dict()["create_time"] if historys else _dict["create_time"]
        _dict["modify_uid"] = historys[-1].to_dict()["create_uid"] if historys else _dict["create_uid"]

        return _dict
