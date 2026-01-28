import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from authx.exceptions import AuthXException
from .soundtracks import router as soundtracks_router
from .auth import router as auth_router
from .config import Config


API_V1_PREFIX = '/api/v1'

def create_app() -> FastAPI:

    os.makedirs(Config.load().files.path, exist_ok=True)

    app = FastAPI()
    app.include_router(soundtracks_router, prefix=API_V1_PREFIX)
    app.include_router(auth_router, prefix=API_V1_PREFIX)
    app.add_exception_handler(AuthXException, auth_exception_handler)

    return app


async def auth_exception_handler(request: Request, exc: AuthXException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Authentication error: {exc}"},
        headers={"WWW-Authenticate": "Bearer"},
    )

