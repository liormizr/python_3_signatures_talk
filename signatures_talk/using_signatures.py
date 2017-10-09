"""
The idea from this talk
David Beazley 2013 talk
Python 3 Metaprogramming: https://www.youtube.com/watch?v=sPiWg5jSoZI
(NOTE: it's a 3 hours talk)

Django’s authentication system
Django auth application:
https://docs.djangoproject.com/en/1.11/ref/contrib/auth/
"""
from contextlib import suppress
from . import include


@include
def data_structures():
    """
    Data structure for Internet provider
    """
    from typing import List
    class Permission:
        def __init__(self, name: str, table: str, code: int):
            self.name = name
            self.table = table
            self.code = code

    class Group:
        def __init__(self, name: str, permissions: List[Permission]):
            self.name = name
            self.permissions = permissions

    class User:
        def __init__(self, name: str, email: str, password: str, groups: List[Group]=()):
            self.name = name
            self.email = email
            self.password = password
            self.groups = groups


def data_structures_for_lazy():
    class Structure:
        _FIELDS = ()
        def __init__(self, *args):
            for name, value in zip(type(self)._FIELDS, args):
                setattr(self, name, value)

    class User(Structure):
        _FIELDS = ('name', 'email', 'password', 'groups')

    class Group(Structure):
        _FIELDS = ('name', 'permissions')

    class Permission(Structure):
        _FIELDS = ('name', 'table', 'code')

    user = User('Name', 'test@gmail.com', '123456', [])
    print(user.name)
    print(user.email)
    print(user.password)
    print(user.goups)

    # issues?
    # help won't work,
    # checking!...
    # demo 1:
    user = User('Name', 100)
    print(user.name)
    print(user.email)
    with suppress(AttributeError):
        print(user.password)
    # no keywords...
    # demo 2:
    with suppress(TypeError):
        user = User(name='Name')
    # no signature
    from inspect import signature
    print(signature(user))


def data_structures_with_signature():
    from typing import List
    from inspect import Parameter, Signature
    class Structure:
        def __init__(self, *args, **kwargs):
            bound_arguments = self.__signature__.bind(*args, **kwargs)
            for name, value in bound_arguments.arguments.items():
                setattr(self, name, value)

    class Permission(Structure):
        __signature__ = Signature(parameters=(
            Parameter('name', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('table', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('code', Parameter.POSITIONAL_OR_KEYWORD, annotation=int),
        ))

    class Group(Structure):
        __signature__ = Signature(parameters=(
            Parameter('name', Parameter.POSITIONAL_OR_KEYWORD, annotation=int),
            Parameter('permissions', Parameter.POSITIONAL_OR_KEYWORD, annotation=List[Permission]),
        ))

    class User(Structure):
        __signature__ = Signature(parameters=(
            Parameter('name', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('email', Parameter.KEYWORD_ONLY, annotation=str),
            Parameter('password', Parameter.KEYWORD_ONLY, annotation=str),
            Parameter('groups', Parameter.KEYWORD_ONLY, annotation=List[Group], default=()),
        ))

    user = User('Name', 'test@gmail.com', '123456', [])
    print(user.name)
    print(user.email)
    print(user.password)
    print(user.goups)

    # issues?
    # help won't work,
    # checking!...
    # demo 1:
    user = User('Name', 100)
    print(user.name)
    print(user.email)
    with suppress(AttributeError):
        print(user.password)
    # no keywords...
    # demo 2:
    with suppress(TypeError):
        user = User(name='Name')
    # no signature
    from inspect import signature
    print(signature(user))

    user.name = 36
    print(user.name)


def data_structures_with_signature_AND_descriptor():
    """
    https://docs.python.org/3.6/howto/descriptor.html
    """
    from typing import TypingMeta, List
    from inspect import Parameter, Signature
    class Field(Parameter):
        def __get__(self, instance, owner=None):
            if instance is None:
                return self
            cache_name = f'_{self.name}_cache'
            cache = getattr(instance, cache_name, self.default)
            if cache is self.empty:
                raise AttributeError(f'no {self.name} found')
            return cache

        def __set__(self, instance, value):
            annotation = self.annotation
            if isinstance(annotation, TypingMeta):
                value_type = annotation.__extra__
                children_types = annotation.__args__ or ()
            else:
                value_type = annotation
                children_types = ()
            if not isinstance(value, value_type):
                raise TypeError(f'invalid value {value} set to {self.name}')
            if children_types and not isinstance(value, children_types):
                raise TypeError(f'invalid children values {value} set to {self.name}')
            cache_name = f'_{self.name}_cache'
            setattr(instance, cache_name, value)

    class StructureMeta(type):
        def __new__(mcs, name, bases, class_dict):
            cls = super().__new__(mcs, name, bases, class_dict)
            cls.__signature__ = Signature(
                field
                for field in class_dict.values()
                if isinstance(field, (Parameter, Field))
            )
            return cls

    class Structure(metaclass=StructureMeta):
        def __init__(self, *args, **kwargs):
            bound_arguments = self.__signature__.bind(*args, **kwargs)
            for name, value in bound_arguments.arguments.items():
                setattr(self, name, value)

    class Permission(Structure):
        name = Field('name', Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
        table = Field('table', Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
        code = Field('code', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)

    class Group(Structure):
        name = Field('name', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)
        permissions = Field('permissions', Parameter.POSITIONAL_OR_KEYWORD, annotation=List[Permission])

    class User(Structure):
        name = Field('name', Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
        email = Field('email', Parameter.KEYWORD_ONLY, annotation=str)
        password = Field('password', Parameter.KEYWORD_ONLY, annotation=str)
        groups = Field('groups', Parameter.KEYWORD_ONLY, annotation=List[Group], default=())
