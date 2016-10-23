import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email
        }

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    items = relationship('Artist', cascade="all, delete-orphan")
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    user_id = Column(Integer, ForeignKey('users.id'))    
    genre = relationship(Genre)
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'genre_id': self.genre_id
        }


# Actual database URL hidden from public repo

engine = create_engine('xxx')
Base.metadata.create_all(engine)