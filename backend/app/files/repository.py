import os
from uuid import uuid4
from typing import Annotated

from fastapi import UploadFile, Depends

from ..database import DBSession
from ..models import File, FileType

class FilesRepository:
    def __init__(self, session: DBSession):
        self._session = session

    def add(self, track_id: int, file: UploadFile, file_type: FileType = FileType.sound) -> File:
        _, ext = os.path.splitext(file.filename)
        db_file = File(
            storage_filename=f'{uuid4()}.{ext}',
            original_filename=file.filename,
            soundtrack_id=track_id,
            file_type=file_type.value,
        )
        self._session.add(db_file)
        self._session.commit()
        self._session.refresh(db_file)
        
        return db_file
    
    def get_by_track_id(self, track_id: int, file_type: FileType) -> File:
        return self._session.query(File).filter_by(soundtrack_id=track_id, file_type=file_type.value).first()
    
    def update(self, track_id: int, file: UploadFile, file_type: FileType) -> File:
        db_file = self._session.query(File).filter_by(soundtrack_id=track_id, file_type=file_type.value).first()

        db_file.original_filename=file.filename

        self._session.commit()
        self._session.refresh(db_file)

        return db_file
    
FilesRepositoryDependency = Annotated[FilesRepository, Depends(FilesRepository)]