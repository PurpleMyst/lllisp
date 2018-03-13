#!/usr/bin/env python3
# I think this module would really benefit from Python 3.7's dataclasses.
import collections

__all__ = ["Symbol", "Number", "String", "SExpr"]

Symbol = collections.namedtuple("Symbol", "value")
Number = collections.namedtuple("Number", "value")
String = collections.namedtuple("String", "value")


class SExpr(collections.namedtuple("SExpr",  "value next")):
    def __iter__(self):
        return SEXprIterator(self)

    def __bool__(self):
        return self is not _empty_sexpr

    @classmethod
    def singleton(cls, value):
        return cls(value, _empty_sexpr)

    @classmethod
    def from_iterable(cls, iterable):
        iterable = iter(iterable)

        try:
            return cls(next(iterable), cls.from_iterable(iterable))
        except StopIteration:
            return _empty_sexpr


class SEXprIterator:
    def __init__(self, sexpr):
        self.sexpr = sexpr

    def __iter__(self):
        return self

    def __next__(self):
        if self.sexpr:
            value = self.sexpr.value
            self.sexpr = self.sexpr.next
            return value
        else:
            raise StopIteration


_empty_sexpr = SExpr(None, None)
