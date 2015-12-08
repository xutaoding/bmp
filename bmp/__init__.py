# coding: utf-8
from myapp import Myapp

import sys

reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(1000000)

app = Myapp.get_instance(__name__)
db = app.db
log = app.logger
cache = app.cache
