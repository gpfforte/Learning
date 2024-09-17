from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ARRAY, TIMESTAMP
from sqlalchemy.orm import sessionmaker, mapper

metadata = MetaData()
person_table = \
    Table('people', metadata,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('name', String(255)),
          Column('age', Integer),
          Column('hobbies', ARRAY(String)),
          Column('birthday', TIMESTAMP)
          )

@dataclass
class Person:
    id: int = None
    name: str = ''
    age: int = 0
    hobbies: List[str] = field(default_factory=list)
    birthday: datetime = field(default_factory=datetime)

@dataclass
class Person:
    id: int = None
    name: str = field(default_factory=str)
    age: int = field(default_factory=int)
    hobbies: List[str] = field(default_factory=list)
    birthday: datetime = field(default_factory=datetime)

@dataclass
class Person:
    id: int = None
    name: str = field(default_factory=lambda: 'john doe')
    age: int = field(default_factory=lambda: 77)
    hobbies: List[str] = field(default_factory=list)
    birthday: datetime = field(default_factory=datetime)

mapper(Person, person_table)

engine = create_engine('postgresql://postgres@localhost:32771/test', echo=True)
metadata.create_all(engine)

session = sessionmaker(bind=engine)()
person = Person(id=None, name='Robby', age=33, hobbies=['golf', 'hiking'], birthday=datetime(1985, 7, 25))
session.add(person)
session.commit()