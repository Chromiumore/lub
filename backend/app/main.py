from fastapi import FastAPI
from .soundtracks import router as soundtracks_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(soundtracks_router)

    return app
