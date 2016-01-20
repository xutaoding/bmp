# coding: utf-8


# todo 自动import modules目录下表定义

from bmp.models import *
from bmp import db

if __name__ == "__main__":
    db.create_all()
