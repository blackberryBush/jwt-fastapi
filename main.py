from fastapi import FastAPI, Header
from fastapi.openapi.models import Response
from pydantic import BaseModel
from starlette import status
from starlette.responses import RedirectResponse, JSONResponse

from tokens import authenticate, token_response


class User(BaseModel):
    name: str
    password: str

    def is_in_base(self) -> bool:
        if self in db.values():
            return True
        return False

    def check_password(self) -> bool:
        pass_from_db = db.get(self.name)
        if pass_from_db != self.password:
            return False


db = {}
app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse("/docs", status_code=status.HTTP_308_PERMANENT_REDIRECT)


@app.post("/login")
async def register(user: User):
    if user.is_in_base():
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db[user.name] = user.password
    return token_response(user)


@app.get("/login/{user_id}")
async def login(user: User):
    if user.check_password():
        return "jwt"
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@app.patch("/login/{user_id}")
async def change_password(user_id: str, user: User, authorization: str = Header()):
    if not authenticate(authorization, user_id):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "authorization error"})
    db[user.name] = user.password
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "password has been changed successfully"})
