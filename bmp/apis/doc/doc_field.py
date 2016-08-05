# coding=utf-8

from bmp.apis.doc.base import BaseDocApi
from bmp.const import DOC
from bmp.models.doc import DocField


class Doc_fieldApi(BaseDocApi):
    route = ["/doc/field", "/doc/field/<int:page>/<int:pre_page>", "/doc/field/<int:fid>"]

    def get(self, page=None, pre_page=None, fid=None):
        if fid:
            return self.succ(DocField.get(fid))
        return self.succ(DocField.select(
            page,
            pre_page
        ))

    def post(self, fid):
        submit = self.request()
        submit["doc_id"] = fid
        DocField.add(submit, auto_commit=False)
        return self.success(DOC.NEW, DocField, submit)

    def put(self, fid):
        submit = self.request()
        submit["id"] = fid
        df = DocField.edit(submit, auto_commit=False)
        submit["doc_id"] = df.doc_id
        return self.success(DOC.PUT, DocField, submit)

    def delete(self, fid):
        field = DocField.get(fid)
        DocField.delete(fid, auto_commit=False)
        return self.success(DOC.DELETE, DocField, field)
