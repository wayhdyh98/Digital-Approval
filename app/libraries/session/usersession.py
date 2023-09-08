import datetime
import uuid
from flask_login import UserMixin

class User(UserMixin):

    npk = ""
    company = ""
    division = ""
    department = ""
    name = ""
    admin = False

    def __init__(self, id = str(uuid.uuid4())):
        self.id = id
        self.sessiondatetime = datetime.datetime.now().timestamp()
        self.is_active = True
        self.admin = True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_admin(self):
        return self.admin

    # Flask-Login is technically able to support these.
    # We don't swing that way.
    def is_anonymous(self):
        return False