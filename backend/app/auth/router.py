from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from app.auth.repository import UsersRepositoryDependency
from app.auth.schemas import LoginSchema, RegisterSchema
from app.auth.service import AuthServiceDependency, require_refresh_token, require_access_token


router = APIRouter()


@router.post('/register', status_code=201)
def register(user_repo: UsersRepositoryDependency, creds: RegisterSchema):
    user = user_repo.get_by_email(creds.email)
    if user:
        raise HTTPException(status_code=409, detail='A user with this email address already exists.')

    user = user_repo.get_by_username(creds.username)
    if user:
        raise HTTPException(status_code=409, detail='A user with this username already exists.')

    user_repo.add(creds=creds)


@router.post('/login')
def login(auth: AuthServiceDependency, user_repo: UsersRepositoryDependency, creds: LoginSchema):
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
def refresh(auth: AuthServiceDependency,user_repo: UsersRepositoryDependency, payload: Annotated[dict, Depends(require_refresh_token)]):
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
def protected(auth: AuthServiceDependency,user_repo: UsersRepositoryDependency, payload: Annotated[dict, Depends(require_access_token)]):
    try:
        db_user = user_repo.get_by_id(user_id=payload.get('sub'))
        return {"message": f'Hello {db_user.username}!'}
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
