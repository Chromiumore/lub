from pydantic import BaseModel, SecretStr, EmailStr


class SoundtrackSchema(BaseModel):
    name: str
    author_id: int
    track_length: int
    listens: int


class UserLoginSchema(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr
