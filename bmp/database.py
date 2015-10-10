#coding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("bmp.config.Config")
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.String(128),unique=True)
    userPassword=db.Column(db.String(128))
    displayName=db.Column(db.String(128))
    mail=db.Column(db.String(128))
    mobile=db.Column(db.String(128))
    title=db.Column(db.String(128))

    def __init__(self,_dict):
        self.uid=_dict["uid"]
        self.userPassword=_dict["userPassword"]
        self.displayName=_dict["displayName"]
        self.mail=_dict["mail"]
        self.mobile=_dict["mobile"]
        self.title=_dict["title"]

    def __repr__(self):
        return "<User %s>" % (self.displayName)


if __name__=="__main__":
    db.create_all()
