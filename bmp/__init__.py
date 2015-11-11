# coding: utf-8
from myapp import Myapp

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Myapp.get_instance(__name__)
db = app.db
log = app.logger
cache = app.cache
