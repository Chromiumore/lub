import io
from typing import Annotated

from fastapi import UploadFile, Depends

from app.files.minio import MinioClient, get_minio_client

BUCKET_NAME="lub-bucket"

class FileStorage:
    def __init__(self, client: MinioClient):
        self._client = client

    @classmethod
    def init_storage(cls):
        cl = get_minio_client()
        if not cl.bucket_exists(BUCKET_NAME):
            cl.make_bucket(BUCKET_NAME)

    def download(self, filename: str):
        return self._client.get_object(BUCKET_NAME, filename)

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
    