from pydantic import BaseModel, EmailStr

# Base model with shared fields
class UserBase(BaseModel):
    email: EmailStr

# Schema for CREATING a user (Input)
class UserPrivate(UserBase):
    password: str

# Schema for RETURNING a user (Output)
class UserPublic(UserBase):
    id: int
    is_active: bool
