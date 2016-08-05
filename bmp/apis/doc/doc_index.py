# coding=utf-8
from bmp.apis.doc.base import BaseDocApi
from bmp.const import DOC
from bmp.models.doc import DocIndex


class Doc_indexApi(BaseDocApi):
    route = ["/doc/index", "/doc/index/<int:page>/<int:pre_page>", "/doc/index/<int:iid>"]

    def get(self, page=None, pre_page=None, iid=None):
        if iid:
            return self.succ(DocIndex.get(iid))
        return self.succ(DocIndex.select(
            page,
            pre_page
        ))

    def post(self, iid):
        submit = self.request()
        submit["doc_id"] = iid
        index = DocIndex.add(submit)
        return self.success(DOC.NEW, DocIndex, submit)

    def put(self, iid):
        submit = self.request()
        submit["id"] = iid
        dindex = DocIndex.edit(submit, auto_commit=False)
        submit["doc_id"] = dindex.doc_id
        return self.success(DOC.PUT, DocIndex, submit)

    def delete(self, iid):
        index = DocIndex.get(iid)
        DocIndex.delete(iid, auto_commit=False)
        return self.success(DOC.DELETE, DocIndex, index)
