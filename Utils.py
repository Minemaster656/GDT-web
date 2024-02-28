import hashlib
import bcrypt


def hash_SHA3_str(input_string)->str:
    """
    This function takes an input string and returns its SHA3 hash as a hexadecimal string.
    """
    sha3_hash = hashlib.sha3_256()
    sha3_hash.update(input_string.encode('utf-8'))
    hashed_string = sha3_hash.hexdigest()
    return hashed_string


def hash_password(password: str) -> str:
    """
    Hash and salt password string with most robust library i know - BCrypt
    """
    # FIXME: майн, заюзай чекпв из бкрипта и замени второй аргумент на bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), b"$2b$12$RTA7FMF2cU4l8XyqHw1bKe").decode()

def check_password(password: str, hashed: str) -> bool:
    """
    Check if password and hash match.
    No, you can't just do hash(pass) == hashed
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())
