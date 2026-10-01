import io
from typing import Annotated

from fastapi import UploadFile, Depends

from app.files.minio import MinioClient, get_minio_client

BUCKET_NAME="lub-bucket"

class FileStorage:
    def __init__(self, client: MinioClient):
        self._client = client
        self._init_storage()

    def _init_storage(self):
        if not self._client.bucket_exists(BUCKET_NAME):
            self._client.make_bucket(BUCKET_NAME)

    def get_stat(self, filename: str):
        return self._client.stat_object(BUCKET_NAME, filename)

    def stream_file(self, filename: str, chunk_size: int = 1024 * 1024, offset: int = 0, length: int = 0):  
        response = self._client.get_object(BUCKET_NAME, filename, offset=offset, length=length)
        try:
            yield from response.stream(chunk_size)
        finally:
            response.close()
            response.release_conn()

    def upload(self, filename: str, file: UploadFile):
        content = file.file.read()
        file_size = len(content)
        data_stream = io.BytesIO(content)

        self._client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=filename,
            data=data_stream,
            length=file_size,
            content_type=file.content_type
        )

    def delete(self, filename: str):
        self._client.remove_object(
            bucket_name=BUCKET_NAME,
            object_name=filename
        )

FileStorageDependency = Annotated[FileStorage, Depends(FileStorage)]
    