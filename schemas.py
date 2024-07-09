from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class FileBase(BaseModel):
    filename: str
    size: int
    salt: bytes
    key_hash: bytes


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: UUID
    uploaded_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[str] = None


class User(UserBase):
    id: UUID
    created_at: Optional[datetime] = None
    hashed_password: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
