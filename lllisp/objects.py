#!/usr/bin/env python3
# I think this module would really benefit from Python 3.7's dataclasses.
import llvmlite.ir

import collections

__all__ = ["Symbol", "Number", "String", "SExpr",
           "BuiltinFunction", "LLVM_TYPES"]

LLVM_TYPES = {
    "int": llvmlite.ir.IntType(32),
}

Symbol = collections.namedtuple("Symbol", "value")
Number = collections.namedtuple("Number", "value")
String = collections.namedtuple("String", "value")

BuiltinFunction = collections.namedtuple("BuiltinFunction",
                                         "returntype func args")


class SExpr(collections.namedtuple("SExpr",  "value next")):
    _empty_sentinel = object()

    def __iter__(self):
        return SEXprIterator(self)

    def __bool__(self):
        if self.value is not self._empty_sentinel:
            return True
        else:
            assert self.next is None
            return False

    @classmethod
    def singleton(cls, value):
        return cls(value, cls.empty())

    @classmethod
    def from_iterable(cls, iterable):
        iterable = iter(iterable)

        try:
            return cls(next(iterable), cls.from_iterable(iterable))
        except StopIteration:
            return cls.empty()

    @classmethod
    def empty(cls):
        return cls(cls._empty_sentinel, None)


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
