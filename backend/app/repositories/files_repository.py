import os
from uuid import uuid4
from typing import Annotated

from fastapi import UploadFile, Depends

from ..database import DBSession
from ..models import File

class FilesRepository:
    def __init__(self, session: DBSession):
        self._session = session

    def add(self, track_id: int, file: UploadFile) -> File:
        _, ext = os.path.splitext(file.filename)
        db_file = File(
            storage_filename=f'{uuid4()}.{ext}',
            original_filename=file.filename,
            soundtrack_id=track_id,
            file_type='sound',
        )
        self._session.add(db_file)
        self._session.commit()
        self._session.refresh(db_file)
        
        return db_file
    
    def get_by_track_id(self, track_id: int) -> File:
        return self._session.query(File).filter_by(soundtrack_id=track_id).first()
    
    def update(self, track_id: int, file: UploadFile) -> File:
        db_file = self._session.query(File).filter_by(soundtrack_id=track_id).first()

        db_file.original_filename=file.filename

        self._session.commit()
        self._session.refresh(db_file)

        return db_file
    
FilesRepositoryDependency = Annotated[FilesRepository, Depends(FilesRepository)]