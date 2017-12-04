import uuid

from passlib.hash import sha512_crypt

from src.common.database import Database
import src.models.users.constants as UserConstants
import src.models.users.errors as UserErrors
import src.models.alerts.constants as AlertConstants
from src.models.games.game import Game

__author__ = 'hooper-p'


class User(object):
    def __init__(self, f_name, l_name, email, password, admin='No', created_on=None, updated_on=None, phone=None,
                 location=None, _id=None):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = password
        self.admin = admin
        self.created_on = created_on
        self.updated_on = updated_on
        self.phone = phone
        self.location = location
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {} has a given name of {} {}".format(self.email, self.f_name, self.l_name)

    @classmethod
    def get_user_by_email(cls, email):
        user = Database.find_one(UserConstants.COLLECTION, {"email": email})
        return cls(**user if user is not None else None)

    @classmethod
    def get_user_by_id(cls, _id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"_id": _id}))

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError(
                "Email is not recognized.  Please use link below to sign-up if you have not created an account.")
        if not sha512_crypt.verify(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Password does not match the one registered.")

        return True

    @staticmethod
    def new_user_valid(email, password, password2):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError(
                "This email is already registered. Please log in.  You can reset your password here if needed.")
        if password != password2:
            raise UserErrors.PasswordsNotMatch("The passwords entered do not match.  Please try again.")

        return True

    @staticmethod
    def user_default_values():
        alerts = {}
        for a in AlertConstants.ALERTS:
            alerts[a] = 'On'
        attendance = {}
        games = Game.get_all_games()
        for i in games:
            if i.home_team.location == 'Blacksburg, VA':
                attendance[i.game_num] = 'Yes'
            else:
                attendance[i.game_num] = 'No'
        return alerts, attendance

    def save_to_mongo(self):
        Database.update(UserConstants.COLLECTION, {"_id": self._id}, self.json())

    def insert_new_user(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "f_name": self.f_name,
            "l_name": self.l_name,
            "email": self.email,
            "password": self.password,
            "admin": self.admin,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
            "phone": self.phone,
            "location": self.location,
            "_id": self._id
        }
