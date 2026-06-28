from typing import List

from sqlalchemy.orm import selectinload

from app.soundtracks.schemas import SoundtrackSchema, UpdateSoundtrackSchema
from app.database import DBSession
from app.models import Soundtrack

class SoundtracksRepository:
    def __init__(self, session: DBSession):
        self._session = session

    def get(self) -> List[Soundtrack]:
        tracks = self._session.query(Soundtrack).options(selectinload(Soundtrack.author)).all()
        return tracks
    
    def get_by_id(self, track_id: int) -> Soundtrack:
        db_track = self._session.query(Soundtrack).options(selectinload(Soundtrack.author)).filter_by(id=track_id).first()
        return db_track
    
    def add(self, track: SoundtrackSchema) -> Soundtrack:
        track = Soundtrack(
            name=track.name,
            author_id=track.author_id,
            track_length=track.track_length,
        )
        self._session.add(track)
        self._session.commit()
        self._session.refresh(track)

        return track
    
    def update(self, track_id: int, track: UpdateSoundtrackSchema) -> Soundtrack:
        db_track = self._session.query(Soundtrack).options(selectinload(Soundtrack.author)).filter_by(id=track_id).first()
        if not db_track:
            return None
        
        for key, value in track.model_dump().items():
            setattr(db_track, key, value)
        self._session.commit()
        self._session.refresh(db_track)
        return db_track
    
    def delete(self, track_id: int):
        self._session.query(Soundtrack).filter_by(id=track_id).delete()
        self._session.commit()
