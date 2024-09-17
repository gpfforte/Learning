# 1 - imports
from actor import Actor
from base import Session, engine
from contact_details import ContactDetails
from movie import Movie
from datetime import date
from sqlalchemy import inspect, MetaData

# 2 - extract a session
session = Session()

# 3 - extract all movies
movies = session.query(Movie)
print(type(movies))

movies = session.query(Movie).all()
print(type(movies))


# 4 - print movies' details
print('\n### All movies:')
for movie in movies:
    print('')
    print(f'{movie.title} was released on {movie.release_date}')
    print("Actors")
    for actor in movie.actors:
        print(actor)
print('')


# other imports and sections...

# 5 - get movies after 15-01-01
movies = session.query(Movie) \
    .filter(Movie.release_date > date(2015, 1, 1)) \
    .all()

print('### Recent movies:')
for movie in movies:
    print(f'{movie.title} was released after 2015')
print('')

# 6 - movies that Dwayne Johnson participated
the_rock_movies = session.query(Movie) \
    .join(Actor, Movie.actors) \
    .filter(Actor.name == 'Dwayne Johnson') \
    .all()

print('### Dwayne Johnson movies:')
for movie in the_rock_movies:
    print(f'The Rock starred in {movie.title}')
print('')

# 6bis - movies that Dwayne Johnson participated
the_rock_movies = session.query(Actor) \
    .filter(Actor.name == 'Dwayne Johnson').scalar().movies
print(type(the_rock_movies))
# .movies_collection

print('### Dwayne Johnson movies:')
for movie in the_rock_movies:
    print(f'The Rock starred in {movie.title}')
print('')

# 7 - get actors that have house in Glendale
glendale_stars = session.query(Actor) \
    .join(ContactDetails, Actor.contact_details) \
    .filter(ContactDetails.address.ilike('%glendale%')) \
    .all()

print('### Actors that live in Glendale:')
for actor in glendale_stars:
    print(f'{actor.name} has a house in Glendale')
print('')

print("# ALL ACTORS WITH A CONTACT DETAIL")

all_details = session.query(ContactDetails).all()
for detail in all_details:
    print(detail.actor)
print('')

query = session.query(Actor.name, Actor.birthday)
for row in query:
    print(row._asdict())
print('')

query = session.query(Actor)
for row in query:
    print(row.name, row.birthday)
print('')

query = session.query(Actor.name, Actor.birthday)
for row in query:
    print(row.name, row.birthday)
print('')

whalberg = session.query(Actor).filter(Actor.name.ilike('%Wahl%')).one()

for c in inspect(Actor).mapper.column_attrs:
    print(getattr(whalberg, c.key))
    # print(c.key)
    # print(c)
print('')

print(Actor.__table__.columns.keys())
print('')

for c in Actor.__table__.columns.keys():
    print(getattr(whalberg, c))
print('')

for c in Actor.__table__.columns:
    print(c)
print('')

metadata = MetaData(bind=engine)
MetaData.reflect(metadata)
print(repr(metadata.tables[Actor.__tablename__]))
print('')

# print(metadata.tables)
for table in metadata.tables:
    print(table)
print('')
print(dir(metadata))
print(metadata.info)


for table in metadata.sorted_tables:
    print('')
    # print(dir(table))
    print(f"Tabella: {table.name}")
    for c in table.columns:
        # print('')
        print(f"Colonna: {c}")
    for primary_key in table.primary_key:
        print(f"Primary Key: {primary_key}")
    for fkey in table.foreign_keys:
        print(fkey)


# for table in metadata.tables:
#     for c in table.columns:
#         print(c)
# print('')
