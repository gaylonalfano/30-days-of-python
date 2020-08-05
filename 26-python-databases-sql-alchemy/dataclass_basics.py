# # ====== Pre Dataclass objects in 3.7
# # Would have to create a Class like below and overwrite the
# # __init__ method of the class.
# class Movie(object):
#     name: str = "Unknown"
#     genre: str = "Action"

#     def __init__(self, name="", genre="", *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.name = name
#         self.genre = genre
#         # self.genre = kwargs.get("genre")
#         # self.genre = genre  # Another TypeError


# # movie_obj = Movie()
# # print(movie.name) # "Unknown"

# # If I wanted to change the name I can't just do:
# # movie_obj = Movie(name="The Professional")  # TypeError Movie() no args
# # Therefore would have to overwrite the __init__ and set self.name = name.
# # THIS GETS CUMBERSOME! Thankfully 3.7 introduced Dataclass objects.

# # movie_obj = Movie(name="Interstellar")
# # print(movie_obj.name)
# movie_obj = Movie(name="Interstellar", genre="Sci-fi")
# print(movie_obj.name, movie_obj.genre)
# movie_two = Movie("The Professional")  # genre="" even though above "Action"
# print(movie_two.name, movie_two.genre)
# movie_three = Movie("Smurfs", "Family")
# print(movie_three.name, movie_three.genre)


# ====== Dataclass objects post 3.7+
# https://realpython.com/python-data-classes/
from dataclasses import dataclass

"""
NOTES:
    - SQL Alchemy ORM lets us store these dataclass objects
      inside a database instead of just in memory.
"""


@dataclass
class Movie:
    # MUST add typehints and provide a default value if you declare
    name: str = "Unknown"
    genre: str = "Action"
    year: int = None


# movie_one = Movie(name="The Professional")
# print(movie_one.name, movie_one.genre)  # genre="Action"
# movie_two = Movie("Avengers", year=2019)
# print(movie_two.name, movie_two.genre, movie_two.year)
# movie_three = Movie("Smurfs", "Family")
# print(movie_three.name, movie_three.genre)


# === Mapping Python objects to a database via ORM
# NOTE: ys%[ -- wraps {...} with [] in Vim
data: dict = [
    {"name": "Interstellar", "genre": "Sci-fi", "year": 2017},
    {"name": "The Professional", "genre": "Action", "year": 1997},
    {"name": "Joker", "genre": "Action", "year": 2018},
]
