from fastapi import FastAPI
import os
from .soundtracks import router as soundtracks_router
from .config import Config


def create_app() -> FastAPI:

    os.makedirs(Config.load().files.path, exist_ok=True)

    app = FastAPI()
    app.include_router(soundtracks_router)

    return app
