import bcrypt


def hashPassword(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes(password, encoding="utf-8"), salt)
    return str(hashed_password)
