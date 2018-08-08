from src.common.database import Database
import src.models.users.constants as UserConstants


class Cleanup(object):
    @staticmethod
    def add_admin_created_to_user():
        Database.update_many(UserConstants.COLLECTION,
                             {"admin_created": "None"},
                             {"$set": {"admin_created": 'No'}})

    @staticmethod
    def admin_created_not_on_user():
        for doc in Database.find(UserConstants.COLLECTION, {"admin_created": {"$exists": False}}):
            print(doc)

