import bcrypt


def hash_password(password: str) -> bytes:
    password: bytes = password.encode('utf-8')
    salt: bytes = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    password: bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
