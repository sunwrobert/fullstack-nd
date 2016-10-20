import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship('Artist', cascade="all, delete-orphan")


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)

engine = create_engine('postgres://mcimbpchmgqyqq:HBafey8eKVFyTioeQFDSq4A3of@ec2-54-235-108-156.compute-1.amazonaws.com:5432/da1i6798elg6el')
Base.metadata.create_all(engine)