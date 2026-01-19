from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return to client (public)
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Properties stored in DB
class UserInDB(User):
    hashed_password: str