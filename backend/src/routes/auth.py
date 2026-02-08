from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Annotated
from ..models import UserCreate, User, UserPublic
from ..db import get_session
from ..auth.auth_handler import get_password_hash, create_access_token, verify_password, authenticate_user
from datetime import timedelta
from ..auth.auth_handler import get_current_user


router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, session: Annotated[AsyncSession, Depends(get_session)]):
    # Check for existing user
    statement = select(User).where(User.email == user.email)
    result = await session.exec(statement)
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Generate JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"data": {"token": access_token, "user": db_user}}

@router.post("/login")
async def login(user_credentials: UserCreate, session: Annotated[AsyncSession, Depends(get_session)]):
    # Authenticate user using the centralized auth function
    user = await authenticate_user(session, user_credentials.email, user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"data": {"token": access_token, "user": user}}

@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information based on the provided token"""
    return current_user

@router.post("/signout")
async def signout():
    """Signout endpoint"""
    return {"message": "Successfully signed out. Please remove the token from your client-side storage."}