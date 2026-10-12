from argon2 import PasswordHasher
from fastapi import APIRouter, Form, HTTPException, status

from app import database

router = APIRouter()
password_hasher = PasswordHasher()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(username: str = Form(...), password: str = Form(...)) -> dict[str, str]:
    user = database.users.find_one({"username": username})
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    database.users.insert_one(
        {"username": username, "password": password_hasher.hash(password)}
    )
    return {"message": f"Welcome, {username}"}