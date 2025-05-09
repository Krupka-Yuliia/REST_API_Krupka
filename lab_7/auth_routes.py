from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from auth import (
    REFRESH_SECRET_KEY,
    ALGORITHM,
    create_access_token,
    create_refresh_token,
    create_http_exception,
)
from database import get_db
from models import User
from schemas import UserDTO, Token, UserCreate

auth = APIRouter(prefix="/v1/api/auth", tags=["authentication"])
password_hasher = CryptContext(schemes=["bcrypt"])


@auth.post("/register", response_model=UserDTO)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.user_name == user.user_name).first():
        raise create_http_exception(status.HTTP_400_BAD_REQUEST, "Username already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise create_http_exception(status.HTTP_400_BAD_REQUEST, "Email already exists")

    new_user = User(
        user_name=user.user_name,
        email=str(user.email),
        hashed_password=password_hasher.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == form_data.username).first()
    if not user or not password_hasher.verify(form_data.password, user.hashed_password):
        raise create_http_exception(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password")

    return {
        "access_token": create_access_token({"sub": user.user_name}),
        "refresh_token": create_refresh_token({"sub": user.user_name}),
        "token_type": "bearer"
    }


@auth.post("/refresh", response_model=Token)
def refresh_token_endpoint(body: dict, db: Session = Depends(get_db)):
    token_str = body.get("refresh_token")
    if not token_str:
        raise create_http_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, "refresh_token is required")

    try:
        payload = jwt.decode(token_str, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise create_http_exception(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")
    except JWTError:
        raise create_http_exception(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")

    user = db.query(User).filter(User.user_name == username).first()
    if not user:
        raise create_http_exception(status.HTTP_401_UNAUTHORIZED, "User not found")

    return {
        "access_token": create_access_token({"sub": username}),
        "refresh_token": create_refresh_token({"sub": username}),
        "token_type": "bearer"
    }
