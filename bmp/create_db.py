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

from bmp import db

if __name__ == "__main__":
    db.create_all()

    # with MySQLdb.connect("192.168.250.10", "ops", "Ops", "bmp_test") as db:
    #     db.execute("show tables;")
    #     for table, in [table for table in db.fetchall() if table != "apscheduler_jobs"]:
    #         db.execute("ALTER TABLE bmp_test.%s ENGINE = InnoDB;" % table)
    #
    # with MySQLdb.connect("192.168.250.10", "ops", "Ops", "bmp") as db:
    #     db.execute("show tables;")
    #     for table, in [table for table in db.fetchall() if table != "apscheduler_jobs"]:
    #         db.execute("ALTER TABLE bmp.%s ENGINE = InnoDB;" % table)
