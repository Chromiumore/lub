from fastapi import FastAPI
import os
from .soundtracks import router as soundtracks_router
from .auth import router as auth_router
from .config import Config

API_V1_PREFIX = '/api/v1'

def create_app() -> FastAPI:

    os.makedirs(Config.load().files.path, exist_ok=True)

    app = FastAPI()
    app.include_router(soundtracks_router, prefix=API_V1_PREFIX)
    app.include_router(auth_router, prefix=API_V1_PREFIX)

    return app
