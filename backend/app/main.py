from fastapi import FastAPI, UploadFile
from .database import db_helper
from .schemas import SoundtrackDTO
from .models import Soundtrack
from .config import Config

app = FastAPI()


@app.get('/')
def index():
    return {'test': 'Hello World!'}


@app.post('/music/', status_code=201)
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


@app.get('/music/{track_id}')
def get(track_id: int):
    with db_helper.session_maker() as session:
        track = session.query(Soundtrack).filter_by(id=track_id).first()
        return {'track': track}


@app.get('/music')
def get_all():
    with db_helper.session_maker() as session:
        tracks = session.query(Soundtrack).all()
        return {'tracks': tracks}


@app.put('/music/{track_id}')
def update(track_id: int, track: SoundtrackDTO):
    with db_helper.session_maker() as session:
        db_track = session.query(Soundtrack).filter_by(id=track_id).first()
        for key, value in track.model_dump().items():
            setattr(db_track, key, value)
        session.commit()
        session.refresh(db_track)
        return {'track': db_track}


@app.delete('/music/{track_id}/')
def delete(track_id: int):
    with db_helper.session_maker() as session:
        session.query(Soundtrack).filter_by(id=track_id).delete()
        session.commit()


@app.post('/upload/')
async def upload_file(file: UploadFile):
    with open(f'{Config.load().files.path}/{file.filename}', 'wb') as out_file:
        content = await file.read()
        out_file.write(content)
