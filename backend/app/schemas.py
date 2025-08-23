from pydantic import BaseModel, SecretStr, EmailStr


class SoundtrackSchema(BaseModel):
    name: str
    author_id: int
    track_length: int
    listens: int


class RegisterSchema(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
