
def include(example):
    suite = example.__module__.split('.')[-1]
    talk_map.setdefault(suite, {'examples': []})
    talk_map[suite]['examples'].append(example)
    return example
talk_map = {}

from . import calling_conventions
from . import inspect_signatures

talk_map['calling_conventions']['sources'] = calling_conventions.__doc__
talk_map['inspect_signatures']['sources'] = calling_conventions.__doc__
