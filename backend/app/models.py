from enum import Enum
from typing import List, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as pgEnum


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Soundtrack(Base):
    __tablename__ = 'soundtracks'

    name: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped['User'] = relationship(back_populates='soundtracks')
    files: Mapped[List['File']] = relationship(back_populates='soundtrack')


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String, unique=True)
    soundtracks: Mapped[List[Soundtrack]] = relationship(back_populates='author')


class FileType(Enum):
    sound = 'sound'
    image = 'image'


class File(Base):
    __tablename__ = 'files'

    storage_filename: Mapped[str] = mapped_column(String, unique=True)
    original_filename: Mapped[str] = mapped_column(String)
    soundtrack_id: Mapped[int] = mapped_column(ForeignKey('soundtracks.id', ondelete='cascade'))
    soundtrack: Mapped[Soundtrack] = relationship(back_populates='files')
    file_type: Mapped[str] = mapped_column(pgEnum(FileType))
    duration: Mapped[Optional[int]] = mapped_column(Integer)
