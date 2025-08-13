from pydantic import BaseModel


class SoundtrackDTO(BaseModel):
    name: str
    author_id: int
    track_length: int
    listens: int
