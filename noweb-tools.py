import DB
import Utils


def putAccessToken(token:str, permissions_values:dict):
    # doc = DB.db_rtb.api_keys.find_one({'token': token})
    # if not doc:
    token_doc = {}
    token_doc = DB.schema(token_doc, DB.Schemes.access_token)
    token_doc['token'] = token
    token_doc['permissions'] = permissions_values

    DB.db_rtb.api_keys.insert_one(token_doc)
    # else:
    #     for k in permissions_values.keys():
    #         doc['permissions'][k] = permissions_values[k]
    #     DB.db_rtb.api_keys.update_one({'token': token}, {'$set': doc})

# putAccessToken(Utils.genToken(3, 8), {"mass_command_api_code": 0})