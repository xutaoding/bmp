from bmp import db

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    uuid = db.Column(db.String(128),unique=True)
    def __init__(self,name,uuid):
        self.uuid=uuid
        self.name=name


    @staticmethod
    def add(name,uuid):
        db.session.add(Upload(name,uuid))
        db.session.commit()



    @staticmethod
    def get_name(uuid):
        if not Upload.query.filter(Upload.uuid==uuid).count():
            return ""
        return Upload.query.filter(Upload.uuid==uuid).one().name
