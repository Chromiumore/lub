from typing import List

from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.soundtracks.schemas import SoundtrackSchema, UpdateSoundtrackSchema
from app.database import DBSession
from app.models import Soundtrack

class SoundtracksRepository:
    def __init__(self, session: DBSession):
        self._session = session

    async def get(self) -> List[Soundtrack]:
        result = await self._session.execute(select(Soundtrack).options(selectinload(Soundtrack.author), selectinload(Soundtrack.files)))
        return result.scalars().all()
    
    async def get_by_id(self, track_id: int) -> Soundtrack:
        result = await self._session.execute(select(Soundtrack).options(selectinload(Soundtrack.author), selectinload(Soundtrack.files)).filter_by(id=track_id))
        return result.scalar_one_or_none()
    
    async def add(self, track: SoundtrackSchema) -> Soundtrack:
        track = Soundtrack(
            name=track.name,
            author_id=track.author_id,
        )
        self._session.add(track)
        await self._session.flush()

        return track
    
    async def update(self, track_id: int, track: UpdateSoundtrackSchema) -> Soundtrack:
        result = await self._session.execute(select(Soundtrack).options(selectinload(Soundtrack.author), selectinload(Soundtrack.files)).filter_by(id=track_id))
        db_track = result.scalar_one_or_none()
        if not db_track:
            return None
        
        for key, value in track.model_dump().items():
            setattr(db_track, key, value)
        await self._session.flush()

        return db_track
    
    async def delete(self, track_id: int):
        db_track = await self._session.get(Soundtrack, track_id)
        await self._session.delete(db_track)
