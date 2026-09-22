from hashlib import sha256
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from app.auth.schemas import RegisterSchema
from app.database import DBSession
from app.models import User

class UsersRepository:
    def __init__(self, session: DBSession):
        self._session = session

    async def get_by_id(self, user_id: int) -> User:
        return await self._session.get(User, user_id)

    async def get_by_email_and_password(self, email: str, password: str) -> User:
        result = await self._session.execute(select(User).filter_by(email=email, password_hash=sha256(password.encode('utf-8')).hexdigest()))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User:
        result = await self._session.execute(select(User).filter_by(email=email))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User:
        result = await self._session.execute(select(User).filter_by(username=username))
        return result.scalar_one_or_none()
    
    async def add(self, creds: RegisterSchema) -> User:
        email = creds.email
        username = creds.username
        password = creds.password.get_secret_value()
        user = User(
                email=email,
                username=username,
                password_hash=sha256(password.encode('utf-8')).hexdigest(),
                )
        self._session.add(user)
        await self._session.flush()
        return user

UsersRepositoryDependency = Annotated[UsersRepository, Depends(UsersRepository)]
