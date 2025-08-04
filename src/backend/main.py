from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Soundtrack(BaseModel):
    name: str
    author: str
    track_length: int
    listens: int
    genres: list | tuple
    album: str | None = None


data = {
    0: Soundtrack(name='Aria 5', author='Joe Fofo', track_length=121, listens=40175, genres=['rock']),
    1: Soundtrack(name='Cake Song', author='Untalanted baker', track_length=307,
                  listens=23, genres=['pop', 'rap'], album='Void'),
}


@app.get('/')
def index():
    return {'test': 'Hello World!'}


@app.post('/music/')
def create(track: Soundtrack):
    data[max(data.keys()) + 1] = track
    return 200


@app.get('/music')
def get():
    return data


@app.get('/music/{track_id}')
def get_all(track_id: int):
    return data[track_id]


@app.put('/music/{track_id}')
def update(track_id: int, track: Soundtrack):
    data[track_id] = track
    return 200


@app.delete('/music/{track_id}')
def delete(track_id: int):
    data.pop(track_id)
    return 200
