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
