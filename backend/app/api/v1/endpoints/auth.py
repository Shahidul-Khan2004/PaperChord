from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserPrivate, UserPublic
from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.security.hashing import Hasher
from app.security.tokens import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

db = Depends(get_db)

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserPrivate, db: AsyncSession = db):
    db_user: RowMapping | None = await UserRepository.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = Hasher.get_password_hash(user.password)
    try:
        new_user = await UserRepository.save_user(db, user_in=user, hashed_password=hashed_password)
        return new_user
    except Exception as e:
        print("Error creating user:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        ) from e
    

@router.post("/login")
async def login_user(user: UserPrivate, db: AsyncSession = db):
    db_user: RowMapping | None = await UserRepository.get_user_by_email(db, email=user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email"
        )
    
    is_verified = Hasher.verify_password(user.password, db_user["hashed_password"])

    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    access_token = create_access_token(data={"sub": db_user["email"]})
    
    return {"access_token": access_token, "token_type": "bearer"}
    