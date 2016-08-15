# coding: utf-8
import os
import uuid
from datetime import datetime

from bmp import app
from bmp.apis.base import BaseApi
from bmp.models.upload import Upload
from flask import request
from flask import send_file


class UploadApi(BaseApi):
    route = ["/upload"]

    def __save_file(self, file):
        path = "%s/%s" % (app.config["UPLOAD_FOLDER"], datetime.now().strftime("%Y-%m-%d"))
        path = path.replace("/", os.sep)
        if not os.path.exists(app.root_path + path):
            os.makedirs(app.root_path + path)

        uid = "%s" % uuid.uuid1()

        Upload.add(file.filename, uid)

        file_path = os.path.join(path, uid)
        file.save(app.root_path + file_path)
        return file_path

    def get(self):
        submit = request.args["path"]
        uuid = submit.split(os.sep)[-1]
        name = Upload.get_name(uuid)
        if not name:
            return send_file(app.root_path + submit, as_attachment=True)
        return send_file(app.root_path + submit, as_attachment=True, attachment_filename=name)

    def post(self):
        _dict = {}
        for name in request.files:
            _dict[name] = self.__save_file(request.files[name])
        return self.succ(_dict)


if __name__ == "__main__":
    print(app.root_path)
