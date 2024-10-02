from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer 
from typing import Optional
from ..config.mt_config import MtConfig as mt_config 


JWT_SECRET = mt_config.JWT_SECRET_KEY
ALGORITHM = mt_config.ALGORITHM

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    payload = decode_jwt(token)
    return payload.get('sub')  # 'sub' is typically used for the user identifier


def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

def create_access_token(user_id: str, email: str, expires_delta: timedelta = None):
    to_encode = {
        "sub": user_id,  # subject claim, typically used for user ID
        "email": email,  # custom claim for email
        "iat": datetime.now(datetime.timezone.utc),  # issued at claim
        "iss": "your-issuer-name",  # issuer claim
        "kid": "your-key-id"  # key ID for Kong
    }
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # expiration claim
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt
