import enum
from pymongo import MongoClient

import config
from userdata import passwd


__client = MongoClient(config.DB_ADDRESS)
__db = __client[config.DB_NAME]

class Schemes(enum.Enum):
    blank = 0
    user = 1


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

def find_one(collection, *args, **kwargs):
    return __db[collection].find_one(*args, **kwargs)

def find_user(udata):
    return find_one("users", udata)

def add_user(username, login, password):
    """
    Adds a new user to the database.

    Args:
        username (str): The username of the new user.
        login (str): The login of the new user.
        password (str): The password of the new user.

    Returns:
        None
    """
    db.users.insert_one(
        schema(
            {"username": username, "login": login, "password": passwd.hash_password(password)},
            Schemes.user
            )
        )