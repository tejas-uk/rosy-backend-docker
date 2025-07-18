import os
from fastapi import APIRouter, Depends, Path, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Optional
from api.db import get_session
from api.models import User, get_utc_now
from pydantic import BaseModel
from jose import JWTError, jwt
import bcrypt
from datetime import timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Replace with a secure key in production
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))

AUTH_TYPE = os.getenv("AUTH_TYPE")


router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = get_utc_now() + expires_delta
    else:
        expire = get_utc_now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Verify JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# 3. Get current user (protected)
def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
    ):
    username = verify_token(token)
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return user


class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class PasswordlessUser(BaseModel):
    username: str




# 1. Register user
@router.post("/register", response_model=Token)
async def register(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    # Update last login time
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password, last_login_at=get_utc_now())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}



# 2. Login user
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # Update last login time
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user.last_login_at = get_utc_now()
    session.add(user)
    session.commit()
    session.refresh(user)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# Endpoints for passwordless auth
@router.post("/passwordless", response_model=Token)
async def passwordless_auth(
    user: PasswordlessUser,
    session: Session = Depends(get_session)
):
    if AUTH_TYPE != "passwordless":
        raise HTTPException(status_code=400, detail="Passwordless auth is not enabled.")
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        # User exists, log them in
        access_token = create_access_token(data={"sub": db_user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    # Register new user
    new_user = User(username=user.username)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Logout user
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    session: Session = Depends(get_session)
):
    return {"detail": "Logged out successfully"}