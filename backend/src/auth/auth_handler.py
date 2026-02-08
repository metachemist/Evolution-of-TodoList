from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from passlib.context import CryptContext
from jose import JWTError, jwt
from .settings import SECRET_KEY, ALGORITHM
from ..models import User
from ..db import get_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    """
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    user = result.first()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the given data and expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    """
    Verify JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
):
    """
    Dependency function to get the current authenticated user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_identifier: str = payload.get("sub")
        if user_identifier is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Determine if the identifier is an email or user ID
    # If it's numeric, treat as user ID; otherwise, treat as email
    if user_identifier.isdigit():
        # Query for the user by ID
        statement = select(User).where(User.id == int(user_identifier))
    else:
        # Query for the user by email
        statement = select(User).where(User.email == user_identifier)

    result = await session.exec(statement)
    user = result.first()

    if user is None:
        raise credentials_exception

    return user