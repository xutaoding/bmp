# coding: utf-8
import MySQLdb

from bmp.models.asset import *
from bmp.models.project import *
from bmp.models.purchase import *
from bmp.models.release import *
from bmp.models.ref import *
from bmp.models.upload import *
from bmp.models.user import *
from bmp.models.leave import *
from bmp.models.idc import *
from bmp.models.report import *
from bmp.models.log import LogSqlalchemy

from bmp import db

if __name__ == "__main__":
    db.create_all()
