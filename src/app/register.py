from fastapi import FastAPI, requests, responses, HTTPException,APIRouter, Request,Form
from argon2 import PasswordHasher # type: ignore
from pymongo import MongoClient


router = APIRouter()
ph= PasswordHasher()

client = MongoClient("mongodb://localhost:27017/")
db= client["NOVA"]
collection= db["users"]

@router.post("/register")
async def login(request:Request,
                username: str= Form(...),
                password: str= Form(...)):
    
    user= collection.find_one({"username":username})
    if user:
        return("Username already taken")
    collection.insert_one("username":username, "password"= ph.hash(password))
    return {"message": f"Welcome, {username}"}    
    