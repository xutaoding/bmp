#coding: utf-8
from myapp import Myapp



app = Myapp(__name__)
db=app.db


app.add_api_rule("/api/login/<string:name>/<string:pwd>","bmp.apis.login")
app.add_api_rule("/api/logout","bmp.apis.logout")
app.add_rule("/","bmp.views.index")
app.add_rule("/service.html","bmp.views.service")


if __name__=="__main__":
    from bmp.models.user import User
    db.create_all()
