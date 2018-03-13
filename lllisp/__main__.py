#!/usr/bin/env python3
import argparse

from .parser import parse
from .compiler import compile_to_ir


def main():
    argp = argparse.ArgumentParser("lllisp")
    argp.add_argument("filename", type=argparse.FileType("r"),
                      help="The file to compile.")
    argv = argp.parse_args()

    with open(argv.filename) as f:
        sexpr = parse(f.read())

    ir = compile_to_ir(sexpr)
    print(ir)


if __name__ == "__main__":
    main()
