#TODO OPTIMIZE
from tinydb import TinyDB, Query
db = TinyDB('db.json')

class User:
    def __init__(self, UUID, auth=False, admin=False):
        results = db.search(Query().UUID == UUID)
        if results and len(results) > 1:
            eprint("More than one DB entry for UUID " + UUID)
            eprint("Panic!")
            exit(1)
        elif results:
            self.UUID = results[0]["UUID"]
            self.auth = results[0]["auth"]
            self.admin = results[0]["admin"]
            #TODO handle consistency here, what if you change auth or admin?
        else:
            data = {}
            data["UUID"] = UUID
            data["auth"] = auth
            data["admin"] = admin
            db.insert(data)

            self.UUID = UUID
            self.auth = auth
            self.admin = admin

    def is_authenticated(self):
        return self.auth

    def is_active(self):
        return self.auth

    def is_anonymous(self):
        return not self.auth

    def get_id(self):
        return self.UUID



