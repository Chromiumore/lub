from pydantic import BaseModel, SecretStr, EmailStr


class RegisterSchema(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr