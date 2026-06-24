from typing import Annotated

from fastapi import UploadFile, File, APIRouter, Body, Depends
from fastapi.responses import StreamingResponse

from .repository import SoundtracksRepository
from ..files.service import FilesServiceDependency
from .schemas import SoundtrackSchema, SoundtrackResponse, UpdateSoundtrackSchema

router = APIRouter()

@router.post('/music/', status_code=201)
async def create(
    track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)],
    files_service: FilesServiceDependency,
    file: UploadFile = File(...),
    track: SoundtrackSchema = Body(...),
):
    db_track = track_repo.add(track=track)

    db_file = files_service.upload_file(file=file, track=db_track)

    return db_track.id


@router.get('/music/{track_id}', response_model=SoundtrackResponse)
def get(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    db_track = track_repo.get_by_id(track_id)
    return db_track


@router.get('/music/{track_id}/file')
def download_file(files_service: FilesServiceDependency, track_id: int):
    response, name = files_service.download_file(track_id)
    return StreamingResponse(
            content=response,
            media_type='application/octet-stream',
            headers={'Content-Disposition': f'attachment; filename="{name}"'}
        )


@router.get('/music', response_model=list[SoundtrackResponse])
def get_all(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)]):
    db_tracks = track_repo.get()
    return db_tracks


@router.put('/music/{track_id}', response_model=SoundtrackResponse)
def update(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int, track: UpdateSoundtrackSchema):
    db_track = track_repo.update(track_id=track_id, track=track)
    return db_track


@router.put('/music/{track_id}/file')
async def update_file(files_service: FilesServiceDependency, track_id: int, file: UploadFile):
    files_service.update_file(track_id=track_id, file=file)


@router.delete('/music/{track_id}/')
def delete(files_service: FilesServiceDependency, track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    files_service.delete_file_from_storage(track_id)

    track_repo.delete(track_id=track_id)
