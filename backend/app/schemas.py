import json
from pydantic import BaseModel, SecretStr, EmailStr, model_validator


class SoundtrackSchema(BaseModel):
    name: str
    author_id: int
    track_length: int
    listens: int

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class RegisterSchema(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
