# Add ability for named arguments
import argparse

# WITH CUSTOM FUNCTIONS:
def my_const_func(*args, **kwargs):
    """My sum() equivalent"""
    print("const:", args, kwargs)


def my_default_func(*args, **kwargs):
    """My default max() equivalent"""
    print("default:", args, kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("integers", type=int, nargs="+")  # + >=1
    # Let's say we want to add up all the ints that are passed
    parser.add_argument(
        "--math",
        dest="math_is_fun",
        action="store_const",
        const=my_const_func,
        default=my_default_func,
    )

    args = parser.parse_args()
    # print(sum(args.integers))
    # print(args.accumulate(args.integers))
    print(args.math_is_fun(args.integers))


# ORIGINAL:
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("integers", type=int, nargs="+")  # + >=1
#     # Let's say we want to add up all the ints that are passed
#     parser.add_argument(
#         "--sum", dest="accumulate", action="store_const", const=sum, default=max
#     )

#     args = parser.parse_args()
#     # print(sum(args.integers))
#     print(args.accumulate(args.integers))


"""
NOTES:
    - Namespace is defined using add_argument("Namespace"). You can
      access it by running print(args.integers) for example:
      [123, 456]
    - If you run nargs='+' for more than one, then args will be a
      t.List object with integers as elements.
    - If you just print(args) then you get: Namespace(integers=[123, 456])
    - The "--sum" argument has to be passed at the end (python % 123 12 --sum)
    - dest=
    - action='store_const' or 'store_true' or 'store_false'
    - const= how are we going to handle this, so can use const=sum for
      the built-in sum() function.
    - default=max to find the max value in the list of integers passed.
    - Basically, 'accumulate' is giving us the option to retrieve max() by
      default OR use the sum() by passing '--sum' at the end. Essentially,
      the --sum argument is assigning sum() (or max() if not passed).
    - args.accumulate(args.integers)
"""
