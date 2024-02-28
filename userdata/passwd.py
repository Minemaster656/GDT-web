import bcrypt

def hash_password(password: str) -> str:
    """
    Hash and salt password string with most robust library i know - BCrypt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed: str) -> bool:
    """
    Check if password and hash match.
    No, you can't just do hash(pass) == hashed
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())
