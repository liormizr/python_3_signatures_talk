"""
First lets talk in the same language
"""
from . import include


@include
def arguments():
    def func(x, y, z):
        ...

    # Positional arguments
    func(1, 2, 3)

    # Keyword arguments
    func(x=1, y=2, z=3)


@include
def default_arguments():
    """
    * Default values set at definition time
    * Only use immutable values (e.g. None, tuple, str, ...)
    """
    def func(x, debug=False, names=()):
        ...

    func(1)
    func(1, debug=True)
    func(1, names=['x', 'y'])


@include
def args_and_kwargs():
    """
    args is tuple of positional arguments.
    kwargs is dict of keyword arguments.
    """
    def func(*args, **kwargs):
        print(f'args={args}')
        print(f'kwargs={kwargs}')
        ...

    func(1, 2, x=3, y=4, z=5)
    # same as:
    func(*(1, 2), **{'x': 3, 'y': 4, 'z': 5})


@include
def keyword_only_arguments():
    """
    * Only in Python 3
    * Named arguments appearing after '*' can only be passed by keyword
    """
    def recv(max_size, *, block=True):
        ...

    def sum(*items, initial=0):
        ...

    recv(1024, block=False)  # Ok
    recv(1024, False)  # Error
