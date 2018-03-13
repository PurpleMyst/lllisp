#!/usr/bin/env python3
from .parser import parse
from .compiler import compile_to_ir


def main():
    with open("example.cl") as f:
        sexpr = parse(f.read())

    ir = compile_to_ir(sexpr)
    print(ir)


if __name__ == "__main__":
    main()
