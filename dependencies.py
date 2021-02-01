from datetime import datetime, timedelta
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# openssl rand -hex 32
SECRET_KEY = "80d6f7b735d046d01bee7615af37e62af64c84666a19fb0f1fe90917637903bb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def