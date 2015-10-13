#coding: utf-8
from bmp import db
from models.user import user_group,Group,User
from models.ref import Ref
from const import REFS
from models.release import Release,ReleaseApproval,ReleaseService

def create_all():
    db.create_all()
    for type,names in REFS.items():
        for name in names:
            db.session.add(Ref(name,type))
    db.session.commit()

if __name__=="__main__":
    create_all()
