#coding: utf-8
from flask import Flask
app = Flask(__name__)


app.config.from_object("bmp.config.Config")

from bmp.views.login import LoginView
app.add_url_rule("/login/<string:user>/<string:pwd>",view_func=LoginView.as_view("login"),methods=["GET","POST"])
