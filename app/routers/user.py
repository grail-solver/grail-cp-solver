import re
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from passlib.hash import pbkdf2_sha256
from datetime import date

from app.db.database import database
from app.utils.customException import EmailSyntaxeError
from app.models.authSchema import LoginSchema
from app.db.tables import Role, users
from app.auth.token_dependency import JWTBearer
from app.auth.token_handler import get_token, add_blacklist_token

EMAIL_PATTERN = re.compile("^[\w\-\.]+@([\w]+\.)+[\w]{2,4}$")
USER_NOT_FOUND_MESSAGE = "User not found! The email address or username is incorrect"

router = APIRouter()


# For user sign up
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request, fullname: str = Form(...), email: str = Form(...), password: str = Form(...),
                   pwd_confirmed: str = Form(...)):
    if not re.match(EMAIL_PATTERN, email):
        raise EmailSyntaxeError()
    if password != pwd_confirmed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Non-compliant passwords")
    hash_pwd = pbkdf2_sha256.hash(password)
    query = users.insert().values(
        name=fullname,
        email=email,
        password=hash_pwd,
        role=Role.common,
        active=1,
        verified=False,
        created_at=date.today()
    )
    try:
        await database.execute(query)
        # await mail_to(fullname, email, request)
        return ({
            "message": "The account has been successfully created! A mail has been sent to you... Check your inbox to verify your email!"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# For user sign in
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(usr: LoginSchema, request: Request):
    query = users.select().where(users.c.email == usr.email)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE)
    if not pbkdf2_sha256.verify(usr.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE)
    if not user.verified:
        # await mail_to(user.name, user.email, request)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Your email address is still not verified! An email has been sent to you to verify it!")
    if not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is no longer active")

    return {"user_id": user.id, "username": user.name, "role": Role[user.role].value, "token": get_token(user.email)}


@router.post("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def logout(req: Request):
    header_param = req.headers.get("Authorization").split(" ")
    if (add_blacklist_token(header_param[1])):
        raise HTTPException(status_code=status.HTTP_200_OK, detail="You hae been logged out successfully")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="An error has occured! Try later")


@router.delete("/delete", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def delete_user(user_id: int = Form(...), user_email: str = Form(...), pwd: str = Form(...)):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE)
    if not pbkdf2_sha256.verify(pwd, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND_MESSAGE)

    query = users.update().where(users.c.id == user_id).values(
        active=0,
        email='[Archived]' + user_email
    )
    await database.execute(query)
    return {
        "removed": True,
        "message": "Your account has been deleted successfully"
    }


@router.put("/update/{user_id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(JWTBearer())])
async def update_profile(user_id: int, fullname: str = Form(...)):
    query = users.update().where(users.c.id == user_id).values(
        name=fullname,
    )
    await database.execute(query)
    query = users.select().where(users.c.id == user_id)
    usr = await database.fetch_one(query)
    return {
        'name': usr.name,
        'email': usr.email,
    }

