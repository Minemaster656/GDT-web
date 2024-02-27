import enum

from pymongo import MongoClient
from private import Core

client = MongoClient(Core.DB_ADDRESS)
db = client[Core.DB_NAME]


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
