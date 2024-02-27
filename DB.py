import enum

from pymongo import MongoClient
from private import Core

client = MongoClient(Core.DB_ADDRESS)
db = client[Core.DB_NAME]

class Schemes(enum.Enum):
    blank=0


def schema(document, scheme):
    fields = {}
    if scheme == Schemes.blank:
        fields = {"field":None}


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
