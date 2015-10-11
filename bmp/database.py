#coding: utf-8
from bmp import db

from models.user import User

if __name__=="__main__":
    db.create_all()
