from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from movie import movies_actors_association
from base import Base


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthday = Column(Date)
    movies = relationship(
        "Movie", secondary=movies_actors_association, back_populates="actors")
    contact_details = relationship("ContactDetails", back_populates="actor")

    def __repr__(self):
        return f"{self.name}"
    # def __init__(self, name, birthday):
    #     self.name = name
    #     self.birthday = birthday
