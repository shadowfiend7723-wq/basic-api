from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Form, HTTPException, status

from app import database

router = APIRouter()
password_hasher = PasswordHasher()


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)) -> dict[str, str]:
    user = database.users.find_one({"username": username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    try:
        password_hasher.verify(user["password"], password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        ) from None

    return {"message": f"Welcome, {username}"}
