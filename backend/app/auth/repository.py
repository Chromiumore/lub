from hashlib import sha256
from typing import Annotated

from fastapi import Depends

from app.auth.schemas import RegisterSchema
from app.database import DBSession
from app.models import User

class UsersRepository:
    def __init__(self, session: DBSession):
        self._session = session

    def get_by_id(self, user_id: int) -> User:
        return self._session.query(User).filter_by(id=user_id).first()

    def get_by_email_and_password(self, email: str, password: str) -> User:
        return self._session.query(User).filter_by(email=email, password_hash=sha256(password.encode('utf-8')).hexdigest()).first()
    
    def add(self, creds: RegisterSchema) -> User:
        email = creds.email
        username = creds.username
        password = creds.password.get_secret_value()
        user = User(
                email=email,
                username=username,
                password_hash=sha256(password.encode('utf-8')).hexdigest(),
                )
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

UsersRepositoryDependency = Annotated[UsersRepository, Depends(UsersRepository)]
