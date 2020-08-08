import sqlite3
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
NOTES:
    - You can reverse engineer the code that made up the database?
      Essentially, how to make SQLA code correspond to a pre-existing
      database (e.g., sqlite:///app.db)? Specifically, the Model code
      that we made to create the tables? Can use a package called
      'sqlacodegen'. In terminal run: 'sqlacodegen sqlite:///app.db'

"""

# Connect to a database by declaring the engine we're using (sqlite3)
# You'd pass in credentials to this engine object
engine = create_engine("sqlite:///app.db")  # mysql, postgres

# Create a Session so we can create datapoints, commit to session, save to db
Session = sessionmaker(bind=engine)
session = Session()


# So, how to turn our Movie Class into a Database table?
# You can't just pass 'object' to Movie(object). Need to use
# SQLA declarative_base()
Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"  # table name

    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)
    year = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Movie name={self.name}, genre={self.genre}, year={self.year}>"
        # <Movie name=Interstellar, genre=Sci-fi, year=2017>


# Add tables to database using metadata
# This will create all models that inherit from Base class
Base.metadata.create_all(engine)


# ======= CREATE/Add an entry/record to our Movie Table
movies = [
    {"name": "Interstellar", "genre": "Sci-fi", "year": 2017},
    {"name": "The Professional", "genre": "Action", "year": 1997},
    {"name": "Joker", "genre": "Action", "year": 2018},
]
# movie_obj = Movie(name="Interstellar", genre="Sci-Fi", year=2016)
# print(movie_obj.name)

# Add multiple movie objects to the session and commit to db
movies_objs = [Movie(**movie) for movie in movies]
# movies_objs = []
# for movie in movies:
#     movie_obj = Movie(**movie)
#     movies_objs.append(movie_obj)
# print(movies_objs)


# Commit the object(s) to our session so we can update/add to database
# session.add(movie_obj)  # Single prepare to save
session.add_all(movies_objs)  # Multiple prepare to save
session.commit()  # save
# print(movie_obj.id)  # 1 -- Now available since it's finally in database


# ======= RETRIEVE item(s) from the database using session.query(Movie).get(id)
# Single item:
# movie_a = session.query(Movie).get(1)
# print(movie_a.id, movie_a.name, movie_a.genre)

# Multiple items: query, queryset, etc.
# q = session.query(Movie).all()  # List
# Filter by a column value using filter_by
# q = (
#     session.query(Movie).filter_by(name="The Professional").all()
# )
# Filter with contains("foo")
# q = (
#     session.query(Movie).filter(Movie.name.contains("Prof")).all()
# )
# Filter by user input() like a search engine for the database
# my_query = input("Query: \n") or "Unknown"
# q = session.query(Movie).filter(Movie.name.contains(my_query)).all()
# q = session.query(Movie).all()
# print(q)


# ======= UPDATE
# # Update single
# movie_to_update = session.query(Movie).get(3)
# movie_to_update.year = 2020
# print(movie_to_update.id, movie_to_update.year)
# session.commit()

# Update multiple
# for movie_obj in q:
#     movie_obj.year = 2021
# session.commit()
# print(session.query(Movie).all())


# ======= DELETE
# Delete all "Interstellar" movies
movies_to_delete = (
    session.query(Movie).filter(Movie.name.contains("Inter")).all()
)
for movie_obj in movies_to_delete:
    session.delete(movie_obj)
session.commit()
session.flush()
print(
    session.query(Movie).filter(Movie.name.contains("Inter")).all()
)  # [] works!
