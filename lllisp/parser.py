#!/usr/bin/env python3
from .objects import Symbol, String, Number, SExpr


def parse(text):
    text = iter(text)

    quoted = False
    buf = []
    result = []

    def push_and_clear_buf(string=False):
        nonlocal quoted, buf

        if not buf:
            return

        buf = "".join(buf)

        if string:
            buf = String(buf)
        else:
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
        elif char == '"':
            push_and_clear_buf()

            escaped = False

            while True:
                char2 = next(text)

                if char2 == '\\':
                    escaped = True
                elif char2 == '"' and not escaped:
                    break
                else:
                    buf.append(char2)

                escaped = False

            push_and_clear_buf(string=True)
        elif char.isspace():
            push_and_clear_buf()
        elif char == '\'':
            quoted = True
        else:
            buf.append(char)

    return SExpr.from_iterable(result)
