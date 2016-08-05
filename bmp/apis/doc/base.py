# coding=utf-8

import json
from datetime import datetime

from bmp import db
from bmp.apis.base import BaseApi
from bmp.const import USER_SESSION
from bmp.models.doc import DocHistory, Doc
from flask import session


class BaseDocApi(BaseApi):
    def success(self, opt, typ, submit):
        if not isinstance(submit, dict):
            doc = Doc.query.filter(Doc.id == submit).one()
        elif submit.__contains__("doc_id"):
            doc = Doc.query.filter(Doc.id == submit.pop("doc_id")).one()
        else:
            doc = Doc.query.filter(Doc.id == submit["id"]).one()

        doc.modify_uid = session[USER_SESSION]["uid"]
        doc.modify_time = datetime.now()

        hist = {
            "content": json.dumps(submit) if isinstance(submit, dict) else "",
            "doc_id": doc.id,
            "type": typ.__name__,
            "opt": opt,
            "create_uid": doc.modify_uid,
            "create_time": doc.modify_time
        }
        DocHistory.add(hist, auto_commit=False)
        db.session.commit()
        return self.succ()


if __name__ == "__main__":
    pass
