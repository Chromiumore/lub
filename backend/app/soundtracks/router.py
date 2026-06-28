from typing import Annotated

from fastapi import UploadFile, File, APIRouter, Body, Form, Depends, Response, status, HTTPException
from fastapi.responses import StreamingResponse

from app.soundtracks.repository import SoundtracksRepository
from app.soundtracks.schemas import SoundtrackSchema, SoundtrackResponse, UpdateSoundtrackSchema
from app.files.service import FilesServiceDependency

router = APIRouter()

ALLOWED_AUDIO_TYPES = {
    'audio/mpeg': 'mp3'
}

ALLOWED_IMAGE_TYPES = {
    'image/jpeg',
    'image/png',
}

@router.post('/music/', status_code=201, response_model=SoundtrackResponse)
async def create(
    track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)],
    files_service: FilesServiceDependency,
    audio_file: UploadFile = File(...),
    cover_image: Annotated[UploadFile | None, File(...)] = None,
    track: SoundtrackSchema = Body(),
):
    if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail='Unsupported audio format')
    
    if cover_image and cover_image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail='Unsupported image format')

    db_track = track_repo.add(track=track)

    await files_service.upload_audio(file=audio_file, track=db_track)

    if cover_image:
        files_service.upload_cover(cover=cover_image, track=db_track)
    
    return db_track


@router.get('/music/{track_id}', response_model=SoundtrackResponse | None)
def get(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    db_track = track_repo.get_by_id(track_id)
    
    if not db_track:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return db_track


@router.get('/music/{track_id}/file')
def download_audio(files_service: FilesServiceDependency, track_id: int):
    res = files_service.download_audio(track_id)
    if not res:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    response, name = res
    return StreamingResponse(
            content=response,
            media_type='application/octet-stream',
            headers={'Content-Disposition': f'attachment; filename="{name}"'}
        )


@router.get('/music/{track_id}/cover')
def download_cover(files_service: FilesServiceDependency, track_id: int):
    res = files_service.download_cover(track_id)
    if not res:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    response, name = res
    return StreamingResponse(
            content=response,
            media_type='application/octet-stream',
            headers={'Content-Disposition': f'attachment; filename="{name}"'}
        )


@router.get('/music', response_model=list[SoundtrackResponse])
def get_all(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)]):
    db_tracks = track_repo.get()
    return db_tracks


@router.put('/music/{track_id}', response_model=SoundtrackResponse | None)
def update(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int, track: UpdateSoundtrackSchema):
    db_track = track_repo.update(track_id=track_id, track=track)
    if not db_track:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return db_track


@router.put('/music/{track_id}/file')
async def update_audio(files_service: FilesServiceDependency, track_id: int, file: UploadFile):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail='Unsupported audio format')
    
    if not await files_service.update_audio(track_id=track_id, file=file):
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/music/{track_id}/cover')
async def update_cover(files_service: FilesServiceDependency, track_id: int, file: UploadFile):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail='Unsupported image format')
    
    if not await files_service.update_cover(track_id=track_id, file=file):
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/music/{track_id}/')
def delete(files_service: FilesServiceDependency, track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    track = track_repo.get_by_id(track_id)
    if not track:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    files_service.delete_file_from_storage(track_id)

    track_repo.delete(track_id=track_id)
