from fastapi import Header, APIRouter
from starlette import status
from starlette.responses import JSONResponse
from starlette.responses import Response

from schemas import User
from services.database_services import add_db, is_in_base, check_password, set_user
from services.jwt_services import get_refresh_token, get_access_token, authenticate, validate_refresh_token

router = APIRouter(tags=["users"])


@router.post("/")
async def signup(user: User):
    if is_in_base(user):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "user is already registered"})
    user_id = add_db(user)
    headers = {"Access-token": get_access_token(user_id),
               "Refresh-token": get_refresh_token(user_id)}
    return Response(headers=headers)


@router.get("/token")
async def refresh(authorization: str = Header()):
    """
    get new access token
    """
    user_id = validate_refresh_token(authorization)
    if user_id == -1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"message": "authorization error"})
    headers = {"Access-token": get_access_token(user_id)}
    return Response(headers=headers)


@router.get("/{user_id}")
async def signin(user: User, user_id: int):
    if check_password(user, user_id):
        headers = {"Access-token": get_access_token(user_id),
                   "Refresh-token": get_refresh_token(user_id)}
        return Response(headers=headers)
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"message": "invalid username or password"})


@router.patch("/{user_id}")
async def change_password(user_id: int, user: User, authorization: str = Header()):
    if not authenticate(authorization, user_id):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"message": "authorization error"})
    set_user(user, user_id)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "password has been changed successfully"})


@router.get("/logout")
async def logout():
    response = Response()
    response.delete_cookie("Authorization")
    return response
