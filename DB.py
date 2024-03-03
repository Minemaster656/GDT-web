import enum

from pymongo import MongoClient

import Utils
from private import Core


client = MongoClient(Core.DB_ADDRESS)
db = client[Core.DB_NAME]
db_rtb=client[Core.DB_RTB_NAME]


class Schemes(enum.Enum):
    blank = 0
    user = 1
    RTB_user = 2

def schema(document, scheme):
    """
    Adjust to the schema for the MongoDB document based on the specified scheme.

    :param document: The document to generate the schema for.
    :param scheme: The scheme to use for generating the schema.
    :return: The adjusted document.
    """
    fields = {}
    if scheme == Schemes.blank:
        fields = {"field": None}
    if scheme == Schemes.user:
        fields={
            "username": None,
            "login": None,
            "password": None
        }
    if scheme == Schemes.RTB_user:
        fields = {"userid": None, "username": " ", "about": None,
                  "age": None, "timezone": None, "color": None,
                  "karma": None, "luck": None, "permissions": None,
                  "money": None, "money_bank": None, "xp": 0, 'banned': 0, 'autoresponder': False,
                  "autoresponder-offline": None, "autoresponder-inactive": None, "autoresponder-disturb": None,
                  "premium_end": 0, "total_reminders": 0, "inventory": {},
                  "birthday_day": 0, "birthday_month": 0, "birthday_year": 0, "activity_changes": []}

    fields_check = {}
    if not document:
        document = fields
    for k in fields.keys():
        fields_check[k] = False
    for k in document.keys():
        if k in fields.keys():
            fields_check[k] = True
    for k in fields_check:
        if not fields_check[k]:
            document[k] = fields[k]
            fields_check[k] = True
    return document
def addUser(username, login, password):
    """
    Adds a new user to the database.

    Args:
        username (str): The username of the new user.
        login (str): The login of the new user.
        password (str): The password of the new user. HASHED!

    Returns:
        None
    """
    doc = db.users.find_one({"login": login})
    if not doc:
        db.users.insert_one(schema({"username": username, "login": login, "password": password}, Schemes.user))
