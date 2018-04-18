import Constants
from SerializableObject import SerializableObject
import dbconn
from werkzeug.security import generate_password_hash, check_password_hash

class User(SerializableObject):
    _UserID       = None
    _UserName     = None
    _UserPassword = None
    _LoggedIn     = False
    _Disabled     = False

    def __init__(self, uid = None, username = None, password = None):
        super(User, self).__init__()

        self._UserID   = uid
        self._UserName = username

        if password is not None:
            self.set_password(password)

    def build_json_dict(self):
        json_dict                  = super(User, self).build_json_dict()
        json_dict['_UserID']       = self._UserID
        json_dict['_UserName']     = self._UserName
        json_dict['_UserPassword'] = self._UserPassword
        json_dict['_LoggedIn']     = self._LoggedIn
        json_dict['_Disabled']     = self._Disabled

        return json_dict

    def build_session_dict(self):
        session_dict = {}
        session_dict['user'] = {}
        session_dict['user']['id']       = self._UserID
        session_dict['user']['name']     = self._UserName
        session_dict['user']['disabled'] = self._Disabled

        return session_dict

    def set_password(self, password):
        self._UserPassword = self.get_hash(password)

    def check_password(self, password):
        return check_password_hash(self._UserPassword, password)

    @staticmethod
    def get_hash(password):
        return generate_password_hash(password)

Constants.SerialObjectTypes.register_type('User', User)
