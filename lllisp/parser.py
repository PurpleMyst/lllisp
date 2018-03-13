#!/usr/bin/env python3
from .objects import Symbol, Number, SExpr


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
