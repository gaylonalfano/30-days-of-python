# Trying the 'src layout'
# Referencing Pyramid setup.py example and SO thread:
# https://github.com/Pylons/pyramid/blob/master/setup.py
# https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
from setuptools import setup, find_packages

setup(
    name="google_geocoding_places_api",
    version="1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
