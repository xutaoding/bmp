# coding: utf-8
from bmp.apis.base import BaseApi
from flask import request
from bmp import app
from datetime import datetime
import os
import uuid
from flask import send_file


class UploadApi(BaseApi):
    route = ["/upload"]

    def __save_file(self, file):
        path = "%s/%s" % (app.config["UPLOAD_FOLDER"], datetime.now().strftime("%Y-%m-%d"))
        path = path.replace("/", os.sep)
        if not os.path.exists(app.root_path+path):
            os.makedirs(app.root_path+path)

        file_path = os.path.join(path, "%s_%s" % (uuid.uuid1(), file.filename))
        file.save(app.root_path+file_path)
        return file_path


    def get(self):
        submit = request.args["path"]
        return send_file(app.root_path+submit,as_attachment=True)

    def post(self):
        _dict = {}
        for name in request.files:
            _dict[name] = self.__save_file(request.files[name])
        return self.succ(_dict)


if __name__=="__main__":
    print(app.root_path)