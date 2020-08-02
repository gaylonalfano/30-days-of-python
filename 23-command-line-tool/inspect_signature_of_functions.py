# Bonus on how to read the arguments of a function
# I read about this previously:
# https://stackoverflow.com/questions/55497837/how-to-tell-a-function-to-use-the-default-argument-values/55498587#55498587
import typing as t
import inspect
from collections import OrderedDict


def random_func(abc, df: str = "123"):
    print(abc, df)


sig: t.OrderedDict = inspect.signature(random_func).parameters
# print(
#     sig
# )  # OrderedDict([('abc', <Parameter "abc">), ('df', <Parameter "df: str = '123'">)])
# print(sig.keys())  # odict_keys(['abc', 'df'])
# print(
#     sig.values()
# )  # odict_values([<Parameter "abc">, <Parameter "df: str = '123'">])


# Here's a function that can help me understand what's happening
def get_signature(fn):
    """
    Separates the default positional and keyword arguments of
    any passed function.

    fn = function to retrieve the signature
    """
    params: t.OrderedDict = inspect.signature(fn).parameters
    args: t.List = []
    kwargs: t.OrderedDict = OrderedDict()
    for p in params.values():
        if p.default is p.empty:
            args.append(p.name)
        else:
            kwargs[p.name] = p.default
    print({"args": args, "kwargs": kwargs})
    # Can see what the default type is for arguments.
    # {'args': ['abc'], 'kwargs': OrderedDict([('df', '123')])}
    return {"args": args, "kwargs": kwargs}


get_signature(random_func)
