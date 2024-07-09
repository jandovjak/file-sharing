from datetime import datetime, timedelta, timezone
from typing import Optional
from config import ALGORITHM, SECRET_KEY

import jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
