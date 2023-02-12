import time
import jwt

from config import SECRET_KEY, ALGORITHM


def get_refresh_token(user_id: int):
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_refresh_token(token: str) -> int:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token.get("user_id", -1)
    except Exception:
        return -1


def authenticate(token: str, user_id: int) -> bool:
    user_id_from_token = validate_access_token(token)
    return user_id_from_token == user_id


def get_access_token(user_id: int):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_access_token(token: str) -> int:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token["user_id"]
        else:
            return -1
    except Exception:
        return -1
