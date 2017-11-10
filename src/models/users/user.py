import uuid

from passlib.hash import sha512_crypt

from src.common.database import Database
import src.models.users.constants as UserConstants
import src.models.users.errors as UserErrors
from src.common.utils import Utils

__author__ = 'hooper-p'


class User(object):
    def __init__(self, f_name, l_name, email, password, admin='No', _id=None):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = password
        self.admin = admin
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {} has a given name of {} {}".format(self.email, self.f_name, self.l_name)

    @classmethod
    def get_user_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

    @classmethod
    def get_user_by_id(cls, _id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"_id": _id}))

    def update_admin(self):
        pass
    # admin saves form to update fields

    def insert_new_user(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "f_name": self.f_name,
            "l_name": self.l_name,
            "email": self.email,
            "password": self.password,
            "admin": self.admin,
            "_id": self._id
        }

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = User.get_user_by_email(email)
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not sha512_crypt.verify(password, user_data.password):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was incorrect.")

        return True
