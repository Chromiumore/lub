from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Soundtrack(Base):
    __tablename__ = 'soundtrack'

    name: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(Integer)
    track_length: Mapped[int] = mapped_column(Integer)
    listens: Mapped[int] = mapped_column(Integer)
