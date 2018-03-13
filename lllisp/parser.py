#!/usr/bin/env python3
import collections

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


def parse(text):
    text = iter(text)

    quoted = False
    buf = []
    result = []

    def push_and_clear_buf():
        nonlocal quoted, buf 

        if not buf:
            return

        buf = "".join(buf)

        if buf.isdigit():
            buf = Number(int(buf))
        else:
            buf = Symbol(buf)

        if quoted:
            buf = ["quote", buf]

        result.append(buf)

        quoted = False
        buf = []

    for char in text:
        if char == '(':
            result.append(parse(text))
        elif char == ')':
            push_and_clear_buf()
            break
        elif char.isspace():
            push_and_clear_buf()
        elif char == '\'':
            quoted = True
        else:
            buf.append(char)

    return SExpr.from_iterable(result)
