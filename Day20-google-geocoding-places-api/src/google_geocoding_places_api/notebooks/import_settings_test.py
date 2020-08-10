# Referencing Pyramid and SO thread:
# https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
# https://github.com/Pylons/pyramid/blob/master/setup.py


# === Will add .../src/google_geocoding_places_api to the SYS.PATH ===
# import os, sys, inspect

# current_dir = os.path.dirname(
#     os.path.abspath(inspect.getfile(inspect.currentframe()))
# )
# print(current_dir)
# # /Users/gaylonalfano/Code/30-days-of-python/Day20-google-geocoding-places-api/src/google_geocoding_places_api/notebooks

# parent_dir = os.path.dirname(current_dir)
# print(parent_dir)
# # /Users/gaylonalfano/Code/30-days-of-python/Day20-google-geocoding-places-api/src/google_geocoding_places_api

# # sys.path.insert(0, parent_dir)  # Add google_geocoding_places_api dir to SYS.PATH
# # print(sys.path.insert(0, parent_dir))  # True
# print(sys.path)


# ======= Trying to import my settings.py from root
# from google_geocoding_places_api.settings import API_KEY  # works!
from google_geocoding_places_api import settings  # works!

api_key = settings.API_KEY
print(api_key)
print(dir())
