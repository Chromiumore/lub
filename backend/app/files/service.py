import os

from fastapi.responses import FileResponse

from ..files.repository import FilesRepositoryDependency
from ..database import DBSession
from ..models import File, Soundtrack
from..config import Config

class FilesService:
    def __init__(self, files_repo: FilesRepositoryDependency):
        self._files_repo = files_repo

    async def upload_file(self, file: File, track: Soundtrack):
        db_file = self._files_repo.add(track_id=track.id, file=file)

        with open(f'{Config.load().files.path}/{db_file.storage_filename}', 'wb') as out_file:
            content = await file.read()
            out_file.write(content)

        return db_file
    
    def download_file(self, track_id: int):
        db_file = self._files_repo.get_by_track_id(track_id=track_id)
        filename = db_file.storage_filename
        
        return FileResponse(f'{Config.load().files.path}/{filename}')
    
    async def update_file(self, file: File):
        with open(f'{Config.load().files.path}/{file.storage_filename}', 'wb') as out_file:
            content = await file.read()
            out_file.write(content)

    def delete_file_from_storage(self, track_id: int):
        db_file = self._files_repo.get_by_track_id(track_id=track_id)
        filename = db_file.storage_filename
        os.remove(f'{Config.load().files.path}/{filename}')
