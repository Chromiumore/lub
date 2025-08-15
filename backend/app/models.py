from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Soundtrack(Base):
    __tablename__ = 'soundtracks'

    name: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    track_length: Mapped[int] = mapped_column(Integer)
    listens: Mapped[int] = mapped_column(Integer)


class User(Base):
    __tablename__ = 'users'

    login: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String, unique=True)
