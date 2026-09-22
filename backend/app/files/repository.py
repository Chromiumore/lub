import os
from uuid import uuid4
from typing import Annotated

from fastapi import UploadFile, Depends
from sqlalchemy import select

from app.database import DBSession
from app.models import File, FileType

class FilesRepository:
    def __init__(self, session: DBSession):
        self._session = session

    async def add(self, track_id: int, file: UploadFile, file_type: FileType = FileType.sound, duration: int = None) -> File:
        _, ext = os.path.splitext(file.filename)
        db_file = File(
            storage_filename=f'{uuid4()}.{ext}',
            original_filename=file.filename,
            soundtrack_id=track_id,
            file_type=file_type.value,
            duration=duration,
        )
        self._session.add(db_file)
        await self._session.flush()
        
        return db_file
    
    async def get_by_track_id(self, track_id: int, file_type: FileType) -> File | None:
        result = await self._session.execute(select(File).filter_by(soundtrack_id=track_id, file_type=file_type.value))
        return result.scalar_one_or_none()
    
    async def update(self, track_id: int, file: UploadFile, file_type: FileType, duration: int = None) -> File | None:
        result = await self._session.execute(select(File).filter_by(soundtrack_id=track_id, file_type=file_type.value))
        db_file = result.scalar_one_or_none()
        if not db_file:
            return None

        db_file.original_filename=file.filename
        if duration:
            db_file.duration = duration

        await self._session.flush()
        await self._session.refresh(db_file)

        return db_file
    
FilesRepositoryDependency = Annotated[FilesRepository, Depends(FilesRepository)]