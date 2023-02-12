from schemas import User

db = {}


def add_db(user: User) -> int:
    len_db = len(db)
    db[len_db] = user
    return len_db


def is_in_base(user: User) -> bool:
    if user in db.values():
        return True
    return False


def check_password(user: User, user_id: int) -> bool:
    user_from_db = db.get(user_id)
    if user_from_db.name != user.name or user_from_db.password != user.password:
        return False
    return True


def set_user(user: User, user_id: int):
    db[user_id] = user
