# coding=utf-8
from bmp.apis.base import BaseApi
from flask import request
from flask import send_from_directory
from bmp import app

class DownloadApi(BaseApi):
    route = ["/download"]

    def get(self):
        submit = request.args["path"]
        return send_from_directory(app.config["UPLOAD_FOLDER"],submit,as_attachment=True)

