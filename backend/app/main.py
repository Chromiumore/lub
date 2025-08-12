from fastapi import FastAPI
from .database import db_helper
from .schemas import SoundtrackDTO
from .database.models import Soundtrack

app = FastAPI()


@app.get('/')
def index():
    return {'test': 'Hello World!'}


@app.post('/music/')
def create(track: SoundtrackDTO):
    with db_helper.session_maker() as session:
        session.add(
            Soundtrack(
                name=track.name,
                author_id=track.author_id,
                track_length=track.track_length,
                listens=track.listens,
            )
        )
        session.commit()


@app.get('/music')
def get():
    return


@app.get('/music/{track_id}')
def get_all(track_id: int):
    return


@app.put('/music/{track_id}')
def update(track_id: int, track: SoundtrackDTO):
    return


@app.delete('/music/{track_id}')
def delete(track_id: int):
    return
