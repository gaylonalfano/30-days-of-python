"""
NOTES:
    - DO NOT CREATE A FILE CALLED pickle.py!
    - Pickles can save STATE so you can pickle some data and pass it around
      and when you open it back up it maintains the original state. This is
      different from a .txt or .csv, since if you later change a data type
      then the CSV won't know/remember but a pickle will.
    - Pandas can save dataframes to pickle objects and then read from pickle
      objects as well. This allows you to pass around a dataframe at some
      particular STATE.
    - Pickles even store the Python data types!
"""
import pickle
import typing as t
import pandas as pd

data = [
    {"name": "Gaylon", "age": 39, "married": True},
    {"name": "Archie", "age": 6, "married": False},
]
# data: t.List[dict] = [
#     {"name": "Gaylon", "age": 39, "married": True},
#     {"name": "Archie", "age": 6, "married": False},
# ]

# Store data inside a pickle 'pkl' file
with open("users.pkl", "wb") as f:
    pickle.dump(data, f)  # not pickle.dumps()!

# Read/load the pickle file.
data_from_pkl = pickle.load(open("users.pkl", "rb"))  # not pickle.loads()!
print(data_from_pkl, type(data_from_pkl))  # <class list>

# Use Pandas to pass around a dataframe stored within a pickle file
df = pd.DataFrame(data)
# print(df.head())
# name  age  married
# 0  Gaylon   39     True
# 1  Archie    6    False

# Use df.to_pickle(). Don't have to add an extension .pkl!
df.to_pickle("df_pkl")

# Use pd.read_pickle() to load in the pickle file.
df2 = pd.read_pickle("df_pkl")
print(df2.head(), df2.dtypes)
"""
     name  age  married
0  Gaylon   39     True
1  Archie    6    False
name       object
age         int64
married      bool
dtype: object
"""
