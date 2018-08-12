import uuid

from passlib.hash import sha512_crypt

import requests

from src.common.database import Database
import src.models.users.constants as UserConstants
import src.models.users.errors as UserErrors
import src.models.alerts.constants as AlertConstants
import src.models.game_preview.constants as PreviewConstants
from src.models.games.game import Game
from src.models.years.year import Year

__author__ = 'hooper-p'


class User(object):
    def __init__(self, f_name, l_name, email, password=None, admin='No', created_on=None, updated_on=None, phone=None,
                 admin_created='No',
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
        self.admin_created = admin_created
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {} has a given name of {} {}".format(self.email, self.f_name, self.l_name)

    @classmethod
    def get_all_users(cls):
        return [cls(**elem) for elem in Database.find(UserConstants.COLLECTION, {})]

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
        admin_created_user = Database.find_one(UserConstants.COLLECTION, {"email": email, "admin_created": "Yes"})
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError(
                "Email is not recognized.  Please use link below to sign-up if you have not created an account.")
        if admin_created_user is not None:
            # Tell the user to sign up
            raise UserErrors.AdminCreatedUserError(
                "Your account was created by an admin.  Please register with HHT to enjoy the full functionality of the site.")
        if not sha512_crypt.verify(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Password does not match the one registered.")

        return True

    @staticmethod
    def check_user_exists(email):
        if Database.find_one(UserConstants.COLLECTION, {"email": email, "admin_created": "No"}) is None:
            return False
        else:
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
    def check_password_strength(password):
        if len(password) < 6:
            UserErrors.PasswordStrength('Your password should be at least 6 characters long.')
        return True

    @staticmethod
    def user_default_values():
        alerts = {}
        for a in AlertConstants.ALERTS:
            alerts[a] = 'On'
        attendance = {}
        games = Game.get_games_by_year(Year.get_current_year()._id)
        for i in games:
            if i.location.city == 'Blacksburg':
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
            "admin_created": self.admin_created,
            "_id": self._id
        }

    def email_password(self, subject, html):
        response = requests.post(PreviewConstants.URL,
                                 auth=('api', PreviewConstants.API_KEY),
                                 data={
                                     "from": PreviewConstants.FROM,
                                     "to": self.email,
                                     "subject": subject,
                                     "html": html
                                 })
        response.raise_for_status()
