from fastapi import FastAPI, UploadFile
from .soundtracks import router as soundtracks_router

app = FastAPI()

app.include_router(soundtracks_router)
