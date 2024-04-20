import bcrypt


def hashPassword(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return str(hashed_password)
