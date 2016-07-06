import json

from bmp import db
from bmp.models.base import BaseModel
from bmp.models.user import User


class Access(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128))
    status = db.Column(db.String(128))
    content = db.Column(db.Text)

    copy_to_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))

    approval_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    approval_time = db.Column(db.DateTime)
    approval_reson = db.Column(db.String(256))

    apply_uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    apply_time = db.Column(db.DateTime)
    apply_reson = db.Column(db.String(256))

    @staticmethod
    def _to_dict(self):
        _dict = self.to_dict()
        _dict["apply_user"] = User.get(_dict["apply_uid"])
        _dict["content"] = json.loads(_dict["content"])
        return _dict
