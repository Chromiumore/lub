from typing import Annotated

from fastapi import Depends
from minio import Minio

from app.config import Config

minio_config = Config.load().s3

MINIO_ENDPOINT=minio_config.endpoint
MINIO_ACCESS_KEY=minio_config.user
MINIO_SECRET_KEY=minio_config.password.get_secret_value()
MINIO_SECURE=False

def get_minio_client() -> Minio:
        return Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )

MinioClient = Annotated[Minio, Depends(get_minio_client)]
