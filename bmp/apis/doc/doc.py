# coding=utf-8

from datetime import datetime

from bmp import db
from bmp.apis.doc.base import BaseDocApi
from bmp.const import DOC, USER_SESSION
from bmp.database import Database
from bmp.models.doc import Doc, DocIndex, DocField
from flask import session


class DocApi(BaseDocApi):
    route = ["/doc", "/doc/<int:page>/<int:pre_page>", "/doc/<int:did>"]

    def get(self, page=None, pre_page=None, did=None):
        if did:
            return self.succ(Doc.get(did))
        return self.succ(Doc.select(
            page,
            pre_page,
            _orders=Doc.modify_time.desc()
        ))

    def post(self):
        submit = self.request()
        indexs = submit.pop("indexs") if submit.__contains__("indexs") else []
        fields = submit.pop("fields") if submit.__contains__("fields") else []

        submit["create_time"] = datetime.now()
        submit["create_uid"] = session[USER_SESSION]["uid"]
        submit["modify_time"] = datetime.now()
        submit["modify_uid"] = session[USER_SESSION]["uid"]

        doc = Doc.add(submit, auto_commit=False)

        doc.indexs = [Database.to_cls(DocIndex, index) for index in indexs]
        doc.fields = [Database.to_cls(DocField, field) for field in fields]

        db.session.commit()
        return self.succ()

    def put(self, did):
        submit = self.request()

        indexs = submit.pop("indexs") if submit.__contains__("indexs") else None
        fields = submit.pop("fields") if submit.__contains__("fields") else None

        submit["id"] = did
        doc = Doc.edit(submit, auto_commit=False)

        if indexs != None:
            doc.indexs = [Database.to_cls(DocIndex, index) for index in indexs]
        if fields != None:
            doc.fields = [Database.to_cls(DocField, field) for field in fields]

        return self.success(DOC.PUT, Doc, submit)

    def delete(self, did):
        Doc.delete(did, auto_commit=False)
        return self.success(DOC.DELETE, Doc, did)


if __name__ == "__main__":
    print Doc.get(3)
