"""
The idea from this talk
David Beazley 2013 talk
Python 3 Metaprogramming: https://www.youtube.com/watch?v=sPiWg5jSoZI
(NOTE: it's a 3 hours talk)
"""
from contextlib import suppress
from . import include


def data_structures():
    class Stock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Address:
        def __init__(self, hostname, port):
            self.hostname = hostname
            self.port = port


def data_structures_for_lazy():
    class Structure:
        _FIELDS = ()

        def __init__(self, *args):
            for name, value in zip(type(self)._FIELDS, args):
                setattr(self, name, value)

    class Stock(Structure):
        _FIELDS = ('name', 'shares', 'price')

    class Point(Structure):
        _FIELDS = ('x', 'y')

    class Address(Structure):
        _FIELDS = ('hostname', 'port')

    s = Stock('Name', 100, 490.5)
    print(s.name)
    print(s.shares)
    print(s.price)

    # issues?
    # help won't work,
    # checking!...
    # demo 1:
    s = Stock('Name', 100)
    print(s.name)
    print(s.shares)
    with suppress(AttributeError):
        print(s.price)
    # no keywords...
    # demo 2:
    with suppress(TypeError):
        s = Stock(name='Name')
    # no signature
    from inspect import signature
    print(signature(s))


def data_structures_with_signature():
    from decimal import Decimal
    from inspect import Parameter, Signature

    class Structure:
        def __init__(self, *args, **kwargs):
            bound_arguments = self.__signature__.bind(*args, **kwargs)
            for name, value in bound_arguments.arguments.items():
                setattr(self, name, value)

    class Stock(Structure):
        __signature__ = Signature(parameters=(
            Parameter('name', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('shares', Parameter.POSITIONAL_OR_KEYWORD, annotation=int),
            Parameter('price', Parameter.POSITIONAL_OR_KEYWORD, annotation=Decimal),
        ))

    class Point(Structure):
        __signature__ = Signature(parameters=(
            Parameter('x', Parameter.POSITIONAL_OR_KEYWORD, annotation=int),
            Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, annotation=int),
        ))

    class Address(Structure):
        __signature__ = Signature(parameters=(
            Parameter('hostname', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('port', Parameter.KEYWORD_ONLY, annotation=int),
        ))

    s = Stock('Name', 100, 490.5)
    print(s.name)
    print(s.shares)
    print(s.price)

    # issues?
    # help won't work,
    # checking!...
    # demo 1:
    s = Stock('Name', 100)
    print(s.name)
    print(s.shares)
    with suppress(AttributeError):
        print(s.price)
    # no keywords...
    # demo 2:
    with suppress(TypeError):
        s = Stock(name='Name')
    # no signature
    from inspect import signature
    print(signature(s))
