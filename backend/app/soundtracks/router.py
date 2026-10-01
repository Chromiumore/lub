import re
from typing import Annotated, Optional
from urllib.parse import quote

from fastapi import UploadFile, File, APIRouter, Body, Query, Depends, Response, status, HTTPException, Header
from fastapi.responses import StreamingResponse

from app.soundtracks.repository import SoundtracksRepository
from app.soundtracks.schemas import SoundtrackSchema, SoundtrackResponse, UpdateSoundtrackSchema
from app.files.service import FilesServiceDependency
from app.models import FileType

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

    db_track = await track_repo.add(track=track)

    await files_service.upload_audio(file=audio_file, track=db_track)

    if cover_image:
        await files_service.upload_cover(cover=cover_image, track=db_track)

    db_track = await track_repo.get_by_id(track_id=db_track.id)
    return db_track


@router.get('/music/{track_id}', response_model=SoundtrackResponse | None)
async def get(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    db_track = await track_repo.get_by_id(track_id)
    
    if not db_track:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return db_track


@router.get('/music/{track_id}/audio')
async def stream_audio(
    files_service: FilesServiceDependency,
    track_id: int,
    range_header: Annotated[Optional[str], Header(alias='Range')] = None
):
    match_range = None
    if range_header:
        match_range = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not match_range:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong range header structure')

    db_file = await files_service.get_by_track_id_and_type(track_id, FileType.audio)
    if not db_file:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    stat = await files_service.get_audio_stat_by_track_id(track_id)
    file_size = stat.size
    content_type = stat.content_type or 'audio/mpeg'

    start = int(match_range.group(1)) if match_range else 0
    end = int(match_range.group(2)) if match_range and match_range.group(2) else file_size - 1
    length = end - start + 1
    status_code = status.HTTP_206_PARTIAL_CONTENT if match_range else status.HTTP_200_OK
    
    response = await files_service.stream_audio(track_id, offset=start, length=length)
    
    return StreamingResponse(
        content=response,
        status_code=status_code,
        media_type=content_type,
        headers={
            'Content-Range': f'bytes {start}-{end}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(length)
        }
    )


@router.get('/music/{track_id}/cover')
async def stream_cover(files_service: FilesServiceDependency, track_id: int):
    db_file = await files_service.get_by_track_id_and_type(track_id, FileType.cover)
    if not db_file:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    response = await files_service.stream_cover(track_id)
    
    return StreamingResponse(
        content=response,
        media_type='application/octet-stream',
        headers={'Content-Disposition': f'attachment; filename="{quote(db_file.original_filename)}"'}
    )


@router.get('/music', response_model=list[SoundtrackResponse])
async def get_all(
    track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)],
    limit: int = Query(ge=1, le=100, default=20),
    offset: int = Query(ge=0, default=0)
):
    db_tracks = await track_repo.get_all(limit=limit, offset=offset)
    return db_tracks


@router.put('/music/{track_id}', response_model=SoundtrackResponse | None)
async def update(track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int, track: UpdateSoundtrackSchema):
    db_track = await track_repo.update(track_id=track_id, track=track)
    if not db_track:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return db_track


@router.put('/music/{track_id}/audio')
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
async def delete(files_service: FilesServiceDependency, track_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], track_id: int):
    track = await track_repo.get_by_id(track_id)
    if not track:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await files_service.delete_file_from_storage(track_id)

    await track_repo.delete(track_id=track_id)
