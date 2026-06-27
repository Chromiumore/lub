import json

from pydantic import BaseModel, model_validator


class SoundtrackSchema(BaseModel):
    name: str
    author_id: int
    track_length: int

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UpdateSoundtrackSchema(BaseModel):
    name: str
    track_length: int

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class SoundtrackResponse(BaseModel):
    id: int
    name: str
    author: UserResponse
    track_length: int

    class Config:
        from_attributes = True
