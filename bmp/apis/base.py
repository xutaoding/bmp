# coding: utf-8
import json
import os
import traceback
from functools import wraps

from bmp import app
from bmp import log
from bmp.const import USER_SESSION
from bmp.utils.exception import ExceptionEx
from flask import jsonify
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask.views import MethodView
from sqlalchemy import or_


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = func(*args, **kwargs).data
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)

    return decorated_function


class BaseApi(MethodView):
    def auth(self):
        session.permanent = True
        if session.__contains__(USER_SESSION):
            return True
        return False

    def dispatch_request(self, *args, **kwargs):
        try:
            if self.auth():
                if request.form.__contains__("method"):
                    method = getattr(self, request.form["method"].lower(), None)
                    return method(*args, **kwargs)
                else:
                    return super(BaseApi, self).dispatch_request(*args, **kwargs)
            else:
                return self.fail("未登录")
        except ExceptionEx, e:
            traceback.print_exc()
            log.exception(e)
            return self.fail(e.message)

        except KeyError, e:
            traceback.print_exc()
            log.exception(e)
            return self.fail("字段 %s 未提交" % e.message)

        except Exception, e:
            traceback.print_exc()
            log.exception(e)
            return self.fail("接口异常", e.__str__())

    def fail(self, error="", msg=""):
        return jsonify({
            "success": False,
            "error": error,
            "message": msg,
            "content": {}
        })

    def get_search_fields(self, _clss, is_fuzzy=True):
        _filters = []

        if not isinstance(_clss, list):
            _clss = [_clss]

        for key in [arg for arg in request.args.keys() if arg != "_"]:
            has_key = False
            for _cls in _clss:
                if not hasattr(_cls, key):
                    continue

                if is_fuzzy:
                    _filters.append(or_(*[
                        getattr(_cls, key).like("%" + arg + "%") for arg in request.args.getlist(key)
                        ]))
                else:
                    _filters.append(or_(*[
                        getattr(_cls, key).like(arg) for arg in request.args.getlist(key)
                        ]))

                has_key = True
                break

            if not has_key:
                raise ExceptionEx("查询字段%s不存在" % key)

        return _filters

    def request(self):
        req = None
        if request.form.__contains__("method"):
            req = request.form["submit"]
        else:
            try:
                req = [request.form[j] for j in request.form][0]
            except Exception, e:
                req = [j for j in request.form][0]

        return json.loads(req)

    def succ(self, data={}, filename=""):
        fdata = ""

        if filename:
            try:
                with open(filename) as fileobj:
                    seek = os.path.getsize(filename) - 1024
                    if seek < 0: seek = 0
                    fileobj.seek(seek)
                    fdata = fileobj.read()
            except:
                raise ExceptionEx("无法读取文件[%s]" % filename)

        return jsonify({
            "success": True,
            "error": "",
            "message": "",
            "content": data,
            "file": fdata
        })

    def redirect(self, url):
        return redirect(url_for(url))

    def dispatch(self):
        pass
