import datetime
from datetime import timedelta, datetime, timezone
from typing import Optional, Literal, Sequence
from hashlib import sha256

import jwt
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic_settings import BaseSettings

from .config import Config
from .schemas import LoginSchema, RegisterSchema
from .database import DBSession
from .models import User


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

    def require_access_token(self, creds: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = creds.credentials   
        payload = self._decode_token(token)
        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type, expected access token'
            )
        return payload
    
    def require_refresh_token(self, creds: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = creds.credentials
        payload = self._decode_token(token)
        if payload.get('type') != 'refresh':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type, expected refresh token'
            )
        return payload
    

auth = AuthService()
auth.load_config(
    config=AuthConfig(
        SECRET_KEY=Config.load().auth.secret_key.get_secret_value()
    )
)

router = APIRouter()


@router.post('/register', status_code=201)
def register(session: DBSession, creds: RegisterSchema):
    email = creds.email
    username = creds.username
    password = creds.password.get_secret_value()
    session.add(
        User(
            email=email,
            username=username,
            password_hash=sha256(password.encode('utf-8')).hexdigest(),
        )
    )
    session.commit()


@router.post('/login')
def login(session: DBSession, creds: LoginSchema):
    email = creds.email
    password = creds.password.get_secret_value()
    db_user = session.query(User).filter_by(email=email, password_hash=sha256(password.encode('utf-8')).hexdigest()).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth.create_access_token(user_id=db_user.id)
    refresh_token = auth.create_refresh_token(user_id=db_user.id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
        }


@router.get('/refresh')
def refresh(session: DBSession, payload: dict = Depends(auth.require_refresh_token)):
    db_user = session.query(User).filter_by(id=payload.get('sub')).first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Bad token. Unable to recognize owner')
    new_access_token = auth.create_access_token(user_id=payload.get('sub'))
    new_refresh_token = auth.create_refresh_token(user_id=payload.get('sub'))
    
    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token
    }


@router.get('/protected')
def protected(session: DBSession, payload: dict = Depends(auth.require_access_token)):
    try:
        db_user = session.query(User).filter_by(id=payload.get('sub')).first()
        return {"message": f'Hello {db_user.username}!'}
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
