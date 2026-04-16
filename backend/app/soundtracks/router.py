import os
from uuid import uuid4
from typing import Annotated

from fastapi import UploadFile, File, APIRouter, Body, Depends
from fastapi.responses import FileResponse

from ..database import DBSession
from ..repositories.soundtracks_repository import SoundtracksRepository
from .schemas import SoundtrackSchema, SoundtrackResponse
from ..models import File as FileDB
from ..config import Config

router = APIRouter()

@router.post('/music/', status_code=201)
async def create(
    session: DBSession,
    track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)],
    file: UploadFile = File(...),
    track: SoundtrackSchema = Body(...),
):
    db_track = track_repo.add(track=track)

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

    return db_track.id


@router.get('/music/{track_id}', response_model=SoundtrackResponse)
def get(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    db_track = track_repo.get_by_id(track_id=track_id)
    return db_track


@router.get('/music/{track_id}/file')
def download_file(session: DBSession, track_id: int):
    db_file = session.query(FileDB).filter_by(soundtrack_id=track_id).first()
    filename = db_file.storage_filename
    
    return FileResponse(f'{Config.load().files.path}/{filename}')


@router.get('/music', response_model=list[SoundtrackResponse])
def get_all(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)]):
    db_tracks = track_repo.get()
    return db_tracks


@router.put('/music/{track_id}', response_model=SoundtrackResponse)
def update(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int, track: SoundtrackSchema):
    db_track = track_repo.update(track_id=track_id, track=track)
    return db_track


@router.put('/music/{track_id}/file')
async def update_file(session: DBSession, track_id: int, file: UploadFile):
    db_file = session.query(FileDB).filter_by(soundtrack_id=track_id).first()

    _, ext = os.path.splitext(file.filename)

    db_file.original_filename=file.filename

    session.commit()

    with open(f'{Config.load().files.path}/{db_file.storage_filename}', 'wb') as out_file:
        content = await file.read()
        out_file.write(content)


@router.delete('/music/{track_id}/')
def delete(session: DBSession, track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    db_file = session.query(FileDB).filter_by(soundtrack_id=track_id).first()
    filename = db_file.storage_filename

    track_repo.delete(track_id=track_id)

    os.remove(f'{Config.load().files.path}/{filename}')
