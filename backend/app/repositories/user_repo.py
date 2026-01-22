from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.schemas.user import UserPrivate

class UserRepository:
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[RowMapping]:
        # We use :email as a named parameter
        query = text("SELECT id, email, hashed_password, is_active FROM users WHERE email = :email")
        result = await db.execute(query, {"email": email})
        
        # .mappings() turns the row into a dictionary-like object
        return result.mappings().fetchone()

    @staticmethod
    async def save_user(db: AsyncSession, user_in: UserPrivate, hashed_password: str) -> Optional[RowMapping]:
        query = text("""
            INSERT INTO users (email, hashed_password)
            VALUES (:email, :hashed_password)
            RETURNING id, email, is_active
        """)
        params = {
            "email": user_in.email, 
            "hashed_password": hashed_password
        }
        result = await db.execute(query, params)
        await db.commit()
        return result.mappings().fetchone()