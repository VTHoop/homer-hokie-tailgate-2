import uuid

from src.common.database import Database
import src.models.alerts.constants as AlertConstants

__author__ = 'hooper-p'


class Alert(object):
    def __init__(self, user, alert, yesno, _id=None):
        self.user = user
        self.alert = alert
        self.yes_no = yesno
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} has alert {} set to {}".format(self.user, self.alert, self.yes_no)

    @staticmethod
    def get_alert_by_user(user):
        return Database.find(AlertConstants.COLLECTION, {"user": user})

    @classmethod
    def get_alert_by_id(cls, id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": id}))

    def update_user_alert_by_id(self, yesno):
        """
        All alerts for a user will be looped through on the view and the ID will be passed with the current yes_no
        flag represented on the form.
        :param id: _id of the alert
        :param yesno: whether the user has selected to receive the alert or not
        :return:
        """
        self.yes_no = yesno
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def insert_alert(self):
        Database.insert(AlertConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "alert": self.alert,
            "yes_no": self.yes_no,
            "user": self.user
        }

