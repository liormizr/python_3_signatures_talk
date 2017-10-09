"""
Source from: https://docs.python.org/3/library/inspect.html
"""
from . import include


@include
def signature_method():
    """
    https://docs.python.org/3/library/inspect.html#introspecting-callables-with-the-signature-object
    New from Python 3.3
    """
    from inspect import signature, Signature

    def func(a, *, b: int, **kwargs) -> bool:
        ...

    func_signature = signature(func)
    assert isinstance(func_signature, Signature)
    print(func_signature)
    print(func_signature.parameters['b'])
    print(func_signature.parameters['b'].annotation)


@include
def modify_signature():
    """
    https://docs.python.org/3/library/inspect.html#inspect.Signature.replace
    """
    from inspect import signature

    def func(a, b):
        ...

    func_signature = signature(func)
    new_func_signature = func_signature.replace(return_annotation="new return anno")
    print(new_func_signature)


@include
def parameters():
    """
    https://docs.python.org/3/library/inspect.html#inspect.Parameter
    """
    from inspect import signature

    def func(a, b, *, c, d=10):
        ...

    func_signature = signature(func)
    for parameter in func_signature.parameters.values():
        if all((parameter.kind == parameter.KEYWORD_ONLY,
                parameter.default is parameter.empty)):
            print(f'Parameter: {parameter}')
