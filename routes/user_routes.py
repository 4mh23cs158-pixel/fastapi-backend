from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import User
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserSchema, UserLogin

router = APIRouter()


@router.post("/signup")
def signup(user: UserSchema, db: Session = Depends(get_db)):
    print(user.model_dump())  # or print(user.dict()) if using Pydantic v1

    repo = UserRepo(db)

    existing_user = repo.get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        phonenumber=user.phonenumber
    )

    print(new_user.name)  # Add this

    repo.create_user(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    repo = UserRepo(db)

    user = repo.get_user_by_email(credentials.email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if user.password != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful"
    }


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return UserRepo(db).get_all_users()


@router.get("/logout")
def logout():
    return {
        "message": "Logout successful"
    }