from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    @staticmethod
    def hash(password: str):
        return pwd_context.hash(password)
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str
    role: str = Field(default="user")
    first_name: str = Field(nullable=True, index=True)
    last_name: str = Field(nullable=True, index=True)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    profile_picture: str = Field(nullable=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class Tasks(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    message: str
    created_at: datetime = Field(default=datetime.now())
    status: Optional[str] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
    completed_by: Optional[int] = None
    completed_at: Optional[datetime] = None

class JwtToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    access_token: str = Field(index=True)
    user_id: int = Field(index=True)
    in_valid: bool = Field(default=False)