from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from ..repositories.user_repository import UserRepositoryDependency
from ..config import Config
from .schemas import LoginSchema, RegisterSchema
from .service import AuthService, AuthConfig
    

auth = AuthService()
auth.load_config(
    config=AuthConfig(
        SECRET_KEY=Config.load().auth.secret_key.get_secret_value()
    )
)

router = APIRouter()


@router.post('/register', status_code=201)
def register(user_repo: UserRepositoryDependency, creds: RegisterSchema):
    user_repo.add(creds=creds)


@router.post('/login')
def login(user_repo: UserRepositoryDependency, creds: LoginSchema):
    email = creds.email
    password = creds.password.get_secret_value()
    db_user = user_repo.get_by_email_and_password(email, password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth.create_access_token(user_id=db_user.id)
    refresh_token = auth.create_refresh_token(user_id=db_user.id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
        }


@router.get('/refresh')
def refresh(user_repo: UserRepositoryDependency, payload: Annotated[dict, Depends(auth.require_refresh_token)]):
    db_user = user_repo.get_by_id(user_id=payload.get('sub'))
    if not db_user:
        raise HTTPException(status_code=400, detail='Bad token. Unable to recognize owner')
    new_access_token = auth.create_access_token(user_id=payload.get('sub'))
    new_refresh_token = auth.create_refresh_token(user_id=payload.get('sub'))
    
    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token
        }


@router.get('/protected')
def protected(user_repo: UserRepositoryDependency, payload: Annotated[dict, Depends(auth.require_access_token)]):
    try:
        db_user = user_repo.get_by_id(user_id=payload.get('sub'))
        return {"message": f'Hello {db_user.username}!'}
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
