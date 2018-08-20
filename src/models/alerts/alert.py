import uuid

from src.common.database import Database
import src.models.alerts.constants as AlertConstants

from src.models.users.user import User

__author__ = 'hooper-p'


class Alert(object):
    def __init__(self, user, alert, yes_no, _id=None):
        self.user = User.get_user_by_id(user)
        self.alert = alert
        self.yes_no = yes_no
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} has alert {} set to {}".format(self.user, self.alert, self.yes_no)

    @classmethod
    def get_alerts_by_user(cls, user):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {"user": user})]

    @classmethod
    def get_alert_by_id(cls, id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": id}))

    @classmethod
    def get_alerts_by_alert_type(cls, alert_type, on_or_off):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"alert": alert_type, "yes_no": on_or_off})]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def remove_alerts(self):
        Database.delete(AlertConstants.COLLECTION, {"_id": self._id})

    @staticmethod
    def remove_alerts_by_user(user_id):
        Database.delete(AlertConstants.COLLECTION, {"user": user_id})

    def json(self):
        return {
            "_id": self._id,
            "alert": self.alert,
            "yes_no": self.yes_no,
            "user": self.user._id
        }
