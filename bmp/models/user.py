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

    @staticmethod
    def join(name,users):
        group=Group.query.filter(Group.name==name).one()
        if users:
            group.users=User.query.filter(User.uid.in_(users)).all()
        else:
            group.users=[]
        db.session.commit()
        return True

    @staticmethod
    def edit(name,new):
        name,new=name.upper(),new.upper()
        group=Group.query.filter(Group.name==name).one()
        group.name=new
        db.session.commit()
        return True

    @staticmethod
    def add(name):
        if Group.query.filter(Group.name==name).count():
            return False
        db.session.add(Group(name))
        db.session.commit()
        return True

    @staticmethod
    def delete(name):
        group=Group.query.filter(Group.name==name).one()
        db.session.delete(group)
        db.session.commit()
        return True

    @staticmethod
    def get(name):
        return Group.query.filter(Group.name.like(name)).one()

    @staticmethod
    def get_users(name):
        return Group.get(name).users


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.String(128),unique=True,nullable=False)
    display_name=db.Column(db.String(128))
    mail=db.Column(db.String(128))
    mobile=db.Column(db.String(128))
    title=db.Column(db.String(128))
    businessCategory=db.Column(db.String(128))
    is_admin=db.Column(db.Boolean)
    create_time=db.Column(db.DateTime)
    last_time=db.Column(db.DateTime)


    def __eq__(self, other):
        return self.uid==other.uid

    def __init__(self,_dict):
        for k,item in _dict.items():
            setattr(self,k,item)


    @staticmethod
    def __add_group(user):
        _user=user.to_dict()
        _user["group"]=[g.name for g in user.groups]
        return _user

    @staticmethod
    def select(uid):
        if uid=="%":
            return [User.__add_group(user) for user in User.query.all()]

        return [User.__add_group(user) for user in User.query.filter(User.uid==uid).all()]


    @staticmethod
    def get(uid):
        user=User.query.filter(User.uid==uid).one()
        return User.__add_group(user)

    @staticmethod
    def edit(uid,email,is_admin):
        user=User.query.filter(User.uid==uid).one()
        user.mail=email
        user.is_admin=is_admin
        db.session.commit()
        return True

    @staticmethod
    def delete(uid):
        user=User.query.filter(User.uid==uid).one()
        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def add(_dict):
        new_user=User(_dict)
        user=User.query.filter(User.uid==new_user.uid)
        if user.count():
            user=user.one()
            user.last_time=datetime.now()
            db.session.commit()
            return True

        new_user.is_admin=False
        new_user.create_time=datetime.now()
        new_user.last_time=datetime.now()
        db.session.add(new_user)
        db.session.commit()
        return True


if __name__=="__main__":
    User.edit("chenglong.yan","test@test.com",1)