from bmp import db
from bmp.models.base import BaseModel


class LogSqlalchemy(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.Text)
    table = db.Column(db.Text)
    object = db.Column(db.Text)
    uid = db.Column(db.String(128), db.ForeignKey("user.uid"))
    create_time = db.Column(db.DateTime)
