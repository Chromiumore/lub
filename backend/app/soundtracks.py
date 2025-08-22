from fastapi import UploadFile, APIRouter
from fastapi.responses import FileResponse
from .database import db_helper
from .schemas import SoundtrackSchema
from .models import Soundtrack
from .config import Config

router = APIRouter()


@router.get('/')
def index():
    return {'test': 'Hello World!'}


@router.post('/music/', status_code=201)
def create(track: SoundtrackSchema):
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


@router.get('/music/{track_id}')
def get(track_id: int):
    with db_helper.session_maker() as session:
        track = session.query(Soundtrack).filter_by(id=track_id).first()
        return {'track': track}


@router.get('/music')
def get_all():
    with db_helper.session_maker() as session:
        tracks = session.query(Soundtrack).all()
        return {'tracks': tracks}


@router.put('/music/{track_id}')
def update(track_id: int, track: SoundtrackSchema):
    with db_helper.session_maker() as session:
        db_track = session.query(Soundtrack).filter_by(id=track_id).first()
        for key, value in track.model_dump().items():
            setattr(db_track, key, value)
        session.commit()
        session.refresh(db_track)
        return {'track': db_track}


@router.delete('/music/{track_id}/')
def delete(track_id: int):
    with db_helper.session_maker() as session:
        session.query(Soundtrack).filter_by(id=track_id).delete()
        session.commit()


@router.post('/upload/')
async def upload_file(file: UploadFile):
    with open(f'{Config.load().files.path}/{file.filename}', 'wb') as out_file:
        content = await file.read()
        out_file.write(content)


@router.get('/download/{filename}')
def download_file(filename: str):
    return FileResponse(f'{Config.load().files.path}/{filename}')