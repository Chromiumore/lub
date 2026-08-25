from typing import Annotated

from fastapi import Depends
from minio import Minio

from app.config import Config, get_config

MINIO_SECURE=False

def get_minio_client(config: Annotated[Config, Depends(get_config)]) -> Minio:
        minio_config = config.s3
        return Minio(
            endpoint=minio_config.endpoint,
            access_key=minio_config.user,
            secret_key=minio_config.password.get_secret_value(),
            secure=MINIO_SECURE
        )

MinioClient = Annotated[Minio, Depends(get_minio_client)]
