#coding: utf-8
from bmp import db

from models.user import User

def create_all():
    db.create_all()
if __name__=="__main__":
    create_all()
