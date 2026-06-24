from typing import Annotated

from fastapi import Depends, UploadFile, Response

from ..files.repository import FilesRepositoryDependency
from .storage import FileStorageDependency
from ..models import File as DBFile, Soundtrack

class FilesService:
    def __init__(self, files_repo: FilesRepositoryDependency, file_storage: FileStorageDependency):
        self._files_repo = files_repo
        self._file_storage = file_storage

    def upload_file(self, file: UploadFile, track: Soundtrack) -> DBFile:
        db_file = self._files_repo.add(track_id=track.id, file=file)

        self._file_storage.upload(db_file.storage_filename, file)

        return db_file
    
    def download_file(self, track_id: int):
        db_file = self._files_repo.get_by_track_id(track_id=track_id)
        filename = db_file.storage_filename
        response = self._file_storage.download(filename)

        return response, db_file.original_filename
    
    def update_file(self, track_id: int, file: UploadFile) -> None:
        db_file = self._files_repo.update(track_id=track_id, file=file)

        self._file_storage.upload(db_file.storage_filename, file)

    def delete_file_from_storage(self, track_id: int) -> None:
        filename = self._files_repo.get_by_track_id(track_id).storage_filename
        self._file_storage.delete(filename)

FilesServiceDependency = Annotated[FilesService, Depends(FilesService)]
