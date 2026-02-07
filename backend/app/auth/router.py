from hashlib import sha256

from fastapi import APIRouter, HTTPException, Depends

from ..config import Config
from .schemas import LoginSchema, RegisterSchema
from ..database import DBSession
from ..models import User
from .service import AuthService, AuthConfig
    

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
