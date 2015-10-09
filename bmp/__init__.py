from flask import Flask
app = Flask(__name__)

from bmp.views.index import IndexView
app.add_url_rule("/",view_func=IndexView.as_view("index"))

from bmp.views.login import LoginView
app.add_url_rule("/login",view_func=LoginView.as_view("login"),methods=["GET","POST"])

from bmp.views.main import MainView
app.add_url_rule("/main",view_func=MainView.as_view("main"))
