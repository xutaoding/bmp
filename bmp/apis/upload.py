# coding: utf-8
from bmp.apis.base import BaseApi
from flask import request
from bmp import app
from datetime import datetime
import os
import uuid
import base64


class UploadApi(BaseApi):
    route = ["/upload"]

    def auth(self):
        return True

    def __save_file(self, file):
        path = "%s%s/%s" % (app.root_path, app.config["UPLOAD_FOLDER"], datetime.now().strftime("%Y-%m-%d"))
        path = path.replace("/", os.sep)
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, "%s_%s" % (uuid.uuid1(), file.filename))
        file.save(file_path)
        return file_path

    def post(self):
        _dict = {}
        for name in request.files:
            _dict[name] = self.__save_file(request.files[name])
        return self.succ(_dict)
