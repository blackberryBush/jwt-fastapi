import jwt
from jwt import DecodeError

from main import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def token_response(user: User):
    return {"access_token": jwt.encode(dict(user), SECRET_KEY, algorithm="HS256")}


def authenticate(token_str: str, user_id: str) -> bool:
    password_from_db = db.get(user_id)
    if password_from_db is None:
        return False
    try:
        decoded = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
    except DecodeError:
        return False
    name = decoded.get("name")
    if name is None or name != user_id:
        return False
    if password_from_db == decoded.get("password"):
        return True
    return False
