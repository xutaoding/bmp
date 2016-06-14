from pymongo import MongoClient


class MongoDB:
    def __init__(self, host, db):
        self.client = MongoClient(host)
        self.db = self.client.get_database(db)

    def __del__(self):
        self.client.close()

    def get_collect(self, collect):
        return self.db.get_collection(collect)
