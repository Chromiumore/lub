import os

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .soundtracks.router import router as soundtracks_router
from .auth.router import router as auth_router
from .files.storage import FileStorage

API_V1_PREFIX = '/api/v1'

def create_app() -> FastAPI:
    FileStorage.init_storage()

    app = FastAPI()
    app.include_router(soundtracks_router, prefix=API_V1_PREFIX)
    app.include_router(auth_router, prefix=API_V1_PREFIX)

    return app
