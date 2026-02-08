import datetime
from datetime import timedelta, datetime, timezone
from typing import Annotated, Optional, Literal, Sequence

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic_settings import BaseSettings

class AuthConfig(BaseSettings):
    ACCESS_TOKEN_EXPIRES: Optional[timedelta] = timedelta(minutes=30)
    REFRESH_TOKEN_EXPIRES: Optional[timedelta] = timedelta(days=7)
    SECRET_KEY: Optional[str] = None
    TOKEN_LOCATION: Sequence[Literal['headers']] = ['headers']
    JWT_ALGORITHM: Optional[Literal['HS256']] = 'HS256'

class AuthService:
    def __init__(self, config: AuthConfig = AuthConfig()):
        self._config = config

    def load_config(self, config: AuthConfig):
        self._config = config

    def create_access_token(self, user_id: int):
        to_encode = {'sub': str(user_id), 'type': 'access'}
        expire = datetime.now(timezone.utc) + self._config.ACCESS_TOKEN_EXPIRES
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._config.SECRET_KEY, algorithm=self._config.JWT_ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: int):
        to_encode = {'sub': str(user_id), 'type': 'refresh'}
        expire = datetime.now(timezone.utc) + self._config.REFRESH_TOKEN_EXPIRES
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._config.SECRET_KEY, algorithm=self._config.JWT_ALGORITHM)
        return encoded_jwt
    
    def _decode_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(jwt=token, key=self._config.SECRET_KEY, algorithms=[self._config.JWT_ALGORITHM])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expired'
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )

    def require_access_token(self, creds: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
        token = creds.credentials   
        payload = self._decode_token(token)
        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type, expected access token'
            )
        return payload
    
    def require_refresh_token(self, creds: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
        token = creds.credentials
        payload = self._decode_token(token)
        if payload.get('type') != 'refresh':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type, expected refresh token'
            )
        return payload