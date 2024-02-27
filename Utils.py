import hashlib


def hash_SHA3_str(input_string)->str:
    """
    This function takes an input string and returns its SHA3 hash as a hexadecimal string.
    """
    sha3_hash = hashlib.sha3_256()
    sha3_hash.update(input_string.encode('utf-8'))
    hashed_string = sha3_hash.hexdigest()
    return hashed_string


