from typing import Annotated

from fastapi import Depends, UploadFile

from app.files.repository import FilesRepositoryDependency
from app.files.storage import FileStorageDependency
from app.models import File as DBFile, Soundtrack, FileType
from app.soundtracks.repository import SoundtracksRepository

class FilesService:
    def __init__(self, files_repo: FilesRepositoryDependency, tracks_repo: Annotated[SoundtracksRepository, Depends(SoundtracksRepository)], file_storage: FileStorageDependency):
        self._files_repo = files_repo
        self._tracks_repo = tracks_repo
        self._file_storage = file_storage

    def _upload(self, file: UploadFile, track: Soundtrack, file_type: FileType) -> DBFile:
        db_file = self._files_repo.add(track_id=track.id, file=file, file_type=file_type)

        self._file_storage.upload(db_file.storage_filename, file)

        return db_file
    
    def _download(self, track_id: int, file_type: FileType):
        db_file = self._files_repo.get_by_track_id(track_id=track_id, file_type=file_type)

        if not db_file:
            return None
        
        filename = db_file.storage_filename
        response = self._file_storage.download(filename)

        return response, db_file.original_filename
    
    def _update(self, track_id: int, file: UploadFile, file_type: FileType) -> None:
        db_file = self._files_repo.update(track_id=track_id, file=file, file_type=file_type)
        if not db_file:
            if self._tracks_repo.get_by_id(track_id):
                db_file = self._files_repo.add(track_id=track_id, file=file, file_type=file_type)
            else:
                return None

        self._file_storage.upload(db_file.storage_filename, file)
        return db_file

    def upload_track_file(self, file: UploadFile, track: Soundtrack) -> DBFile:
        return self._upload(file, track, FileType.sound)
    
    def upload_cover(self, cover: UploadFile, track: Soundtrack) -> DBFile:
        return self._upload(cover, track, FileType.image)
    
    def download_track_file(self, track_id: int):
        return self._download(track_id, FileType.sound)
    
    def download_cover(self, track_id: int):
        return self._download(track_id, FileType.image)
    
    def update_track_file(self, track_id: int, file: UploadFile):
        return self._update(track_id, file, FileType.sound)
    
    def update_cover(self, track_id: int, file: UploadFile):
        return self._update(track_id, file, FileType.image)

    def delete_file_from_storage(self, track_id: int) -> None:
        sound = self._files_repo.get_by_track_id(track_id, FileType.sound)
        cover = self._files_repo.get_by_track_id(track_id, FileType.image)
        self._file_storage.delete(sound.storage_filename)
        if cover:
            self._file_storage.delete(cover.storage_filename)

FilesServiceDependency = Annotated[FilesService, Depends(FilesService)]
