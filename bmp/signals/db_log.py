from bmp.const import USER_SESSION
from flask import session
from datetime import datetime
import MySQLdb
import re
import traceback


def log(app, changes):
    try:
        uri = app.config["SQLALCHEMY_DATABASE_URI"]
        user, passwd, host, _db = re.compile("mysql://(.+):(.+)@(.+):[0-9]+/(.+)").findall(uri)[0]

        if session.__contains__(USER_SESSION):
            with MySQLdb.connect(user=user, passwd=passwd, host=host, db=_db, charset="utf8") as cursor:
                for obj, action in changes:
                    cursor.execute(
                        "insert into log_sqlalchemy "
                        "(`action`,`table`,`object`,`uid`,`create_time`) VALUES (%s,%s,%s,%s,%s)",
                        (action,
                         obj.__class__.__name__,
                         obj._to_dict(obj).__str__(),
                         session[USER_SESSION]["uid"],
                         datetime.now())
                    )
    except Exception, e:
        app.logger.exception(e)
        traceback.print_exc()


if __name__ == "__main__":
    pass
