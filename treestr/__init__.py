import inspect, types

class treestr(str):
    __slots__ = ['parents', 'tags']
    def __new__(cls, s=None, tags=None, parents=None, **kwargs):
        if isinstance(s, treestr):
            return s
        elif s:
            self = super(treestr, cls).__new__(cls, s, **kwargs)
        else:
            self = super(treestr, cls).__new__(cls, **kwargs)
        if tags is None: tags = set()
        if parents is None: parents = tuple()
        self.tags = tags
        self.parents = parents
        return self
    def __radd__(self, other):
        combined = other + str(self)
        return treestr(combined, parents=(self, treestr(other)))
    def __mod__(self, other):
        parents = [self]
        if isinstance(other, str):
            parents.append(treestr(other))
        elif isinstance(other, dict):
            for item in other.values():
                if isinstance(item, str):
                    parents.append(treestr(item))
        elif isinstance(other, tuple):
            for item in other:
                if isinstance(item, str):
                    parents.append(treestr(item))
        return treestr(super().__mod__(other), parents=parents)
    def rtags(self):
        tags = set()
        for parent in self.parents:
            for tag in parent.rtags():
                tags.add(tag)
        for tag in self.tags:
            tags.add(tag)
        return tags

single_fns = ['capitalize', 'casefold', 'expandtabs', 'lower', 'lstrip',
    'rstrip', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill',
    '__getitem__', '__mul__', '__rmul__']
def single(fn):
    def converted(self, *args, **kwargs):
        result = treestr(fn(self, *args, **kwargs), parents=(self,))
        return result
    return converted
for fn_name in single_fns:
    setattr(treestr, fn_name, single(getattr(str, fn_name)))

from_args_fns = ['center', 'ljust', 'rjust', 'zfill', '__add__', 'format']
def parents_from_args(fn):
    def converted(self, *args, **kwargs):
        parents = tuple(treestr(item) for item in args + tuple(kwargs.values()) \
                if isinstance(item, str))
        result = treestr(fn(self, *args, **kwargs), parents=(self,)+parents)
        return result
    return converted
for fn_name in from_args_fns:
    setattr(treestr, fn_name, parents_from_args(getattr(str, fn_name)))

tuple_fns = ['partition', 'rpartition']
def tuple_response(fn):
    def converted(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        return tuple(treestr(i, parents=(self,)) for i in result)
    return converted
for fn_name in tuple_fns:
    setattr(treestr, fn_name, tuple_response(getattr(str, fn_name)))

list_fns = ['split', 'splitlines']
def list_response(fn):
    def converted(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        return [treestr(i, parents=(self,)) for i in result]
    return converted
for fn_name in list_fns:
    setattr(treestr, fn_name, list_response(getattr(str, fn_name)))

from_seq_fns = ['join']
def from_seq(fn):
    def converted(self, *args, **kwargs):
        parents = [self]
        for item in args[0]:
            if isinstance(item, str):
                parents.append(treestr(item))
        return treestr(fn(self, *args, **kwargs), parents=parents)
    return converted
for fn_name in from_seq_fns:
    setattr(treestr, fn_name, from_seq(getattr(str, fn_name)))

