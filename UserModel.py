from flask_login import UserMixin


class UserModel(UserMixin):
    def FromDB(self, user_id, db):
        self.__user = db.query.get(id)
