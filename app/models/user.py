from flask_login import UserMixin
from firebase_admin import auth

class User(UserMixin):
    def __init__(self, uid, email):
        self.id = uid
        self.email = email

    @staticmethod
    def get(user_id):
        try:
            user = auth.get_user(user_id)
            return User(user.uid, user.email)
        except:
            return None