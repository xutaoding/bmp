from bmp import db

class Purchase(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)

    apply_uid=db.Column(db.String(128),nullable=False)
    apply_time=db.Column(db.DateTime,nullable=False)

    def __init__(self):
        pass