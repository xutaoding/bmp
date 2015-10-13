#coding: utf-8
from bmp import db
from datetime import datetime

user_group=db.Table("user_group",
                    db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
                    db.Column("group_id",db.Integer,db.ForeignKey("group.id")))

class Group(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128),unique=True)
    users=db.relationship("User",secondary=user_group,backref=db.backref("groups"))

    def __init__(self,name):
        self.name=name

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.String(128),unique=True)
    display_name=db.Column(db.String(128))
    mail=db.Column(db.String(128))
    mobile=db.Column(db.String(128))
    title=db.Column(db.String(128))
    businessCategory=db.Column(db.String(128))
    is_admin=db.Column(db.Boolean)
    create_time=db.Column(db.DateTime)
    modify_time=db.Column(db.DateTime)

    def __init__(self,_dict):
        for k,lst_item in _dict.items():
            setattr(self,k,lst_item[0])

def add(_dict):
    user=User(_dict)
    user.is_admin=False
    user.create_time=datetime.now()
    user.modify_time=datetime.now()
    db.session.add(user)
    db.session.commit()
    return True

def join_group(name,users):
    group=Group.query.filter(Group.name==name)
    group.users=User.query.filter(User.uid.in_(users)).all()
    db.session.commit()
    return True

def edit_group(name,new):
    group=Group.query.filter(Group.name==new)
    if group.count():
        return False
    group.name=new
    db.session.commit()
    return True


def add_group(name):
    group=Group.query.filter(Group.name==name)
    if group.count():
        return False
    db.session.add(Group(name))
    db.session.commit()
    return True


def edit(uid,email,is_admin):
    user=User.query.filter(User.uid==uid).one()
    user.mail=email
    user.is_admin=is_admin
    db.session.commit()


def delete_group(name):
    group=Group.query.filter(Group.name==name).one()
    db.session.delete(group)
    db.session.commit()
    return True

def delete(uid):
    user=User.query.filter(User.uid==uid).one()
    db.session.delete(user)
    db.session.commit()
    return True


if __name__=="__main__":
    edit("chenglong.yan","test@test.com",1)