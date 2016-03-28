from bmp.const import USER_SESSION
from flask import session
from datetime import datetime
import MySQLdb
import re


def log(app, changes):
    from bmp.models.log import LogSqlalchemy
    #host="localhost",user="root",passwd="sa",db="mytable",charset="utf8"
    uri=app.config["SQLALCHEMY_DATABASE_URI"]
    user,passwd,host,_db=re.compile("mysql://(.+):(.+)@(.+):[0-9]+/(.+)").findall(uri)[0]

    with MySQLdb.connect(user=user,passwd=passwd,host=host,db=_db,charset="utf8") as cursor:
        for obj, action in changes:
            cursor.execute(
                "insert into log_sqlalchemy "
                "(`action`,`table`,`object`,`uid`,`create_time`) VALUES (%s,%s,%s,%s,%s)",
                (action,
                obj.__class__.__name__,
                obj._to_dict(obj).__str__(),
                "chenglong.yan",
                datetime.now())
            )

if __name__=="__main__":
    from flask_sqlalchemy import models_committed
    from bmp import app
    models_committed.connect(log,app)

    from bmp.models.asset import Category

    print Category.edit({"id":51,"name":"441"})