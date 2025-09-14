import os
from uuid import uuid4
from typing import Annotated
from fastapi import UploadFile, File, APIRouter, Body
from fastapi.responses import FileResponse
from .database import db_helper
from .schemas import SoundtrackSchema
from .models import Soundtrack, FileType
from .models import File as FileDB
from .config import Config

router = APIRouter()


@router.get('/')
def index():
    return {'test': 'Hello World!'}


@router.post('/music/', status_code=201)
async def create(
    file: UploadFile = File(...),
    track: SoundtrackSchema = Body(...),
):
    with db_helper.session_maker() as session:
        track = Soundtrack(
                name=track.name,
                author_id=track.author_id,
                track_length=track.track_length,
                listens=track.listens,
            )
        session.add(track)
        session.flush()

        _, ext = os.path.splitext(file.filename)
        db_file = FileDB(
            storage_filename=f'{uuid4()}.{ext}',
            original_filename=file.filename,
            soundtrack_id=track.id,
            file_type='sound',
        )
        session.add(db_file)
        session.commit()

        with open(f'{Config.load().files.path}/{db_file.storage_filename}', 'wb') as out_file:
            content = await file.read()
            out_file.write(content)


@router.get('/music/{track_id}')
def get(track_id: int):
    with db_helper.session_maker() as session:
        track = session.query(Soundtrack).filter_by(id=track_id).first()
        return {'track': track}


@router.get('/music/{track_id}/file')
def download_file(track_id: int):
    with db_helper.session_maker() as session:
        db_file = session.query(FileDB).filter_by(soundtrack_id=track_id).first()
        filename = db_file.storage_filename
        
        return FileResponse(f'{Config.load().files.path}/{filename}')


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


@router.put('/music/{track_id}/file')
async def update_file(track_id: int, file: UploadFile):
    with db_helper.session_maker() as session:
        db_file = session.query(FileDB).filter_by(soundtrack_id=track_id).first()

        _, ext = os.path.splitext(file.filename)

        db_file.original_filename=file.filename

        session.commit()

        with open(f'{Config.load().files.path}/{db_file.storage_filename}', 'wb') as out_file:
            content = await file.read()
            out_file.write(content)


@router.delete('/music/{track_id}/')
def delete(track_id: int):
    with db_helper.session_maker() as session:
        db_file = session.query(FileDB).filter_by(soundtrack_id=track_id).first()
        filename = db_file.storage_filename

        session.query(Soundtrack).filter_by(id=track_id).delete()
        session.commit()
    
        os.remove(f'{Config.load().files.path}/{filename}')
