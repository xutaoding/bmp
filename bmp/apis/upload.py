from bmp.apis.base import BaseApi
from flask import request
import base64
from bmp import app
from datetime import datetime

class UploadApi(BaseApi):
    route=["/upload"]

    def __save_file(self,name,file):
        path="%s%s/%s/%s"%(app.root_path,app.config["UPLOAD_FOLDER"],datetime.now().strftime("%Y-%m-%d"),name)
        file.save(path)
        return {name:base64.b64encode(path)}

    def post(self):
        return self.succ([self.__save_file(name,request.files[name]) for name in request.files])