from bmp import db

class PurchaseSupplier(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128),nullable=False,unique=True)


class PurchaseGoods(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(128))
    price=db.Column(db.Float)
    spec=db.Column(db.String(128))
    amount=db.Column(db.Integer)


class Purchase(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    purpose=db.Column(db.String(128))
    apply_uid=db.Column(db.String(128),nullable=False)
    apply_time=db.Column(db.DateTime,nullable=False)

    def __init__(self):
        pass