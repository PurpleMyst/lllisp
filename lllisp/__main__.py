#!/usr/bin/env python3
import argparse

from .parser import parse
from .compiler import Compiler


def main():
    argp = argparse.ArgumentParser("lllisp")
    argp.add_argument("file", type=argparse.FileType("r"),
                      help="The file to compile.")
    argv = argp.parse_args()

    with argv.file as f:
        program = parse(f.read())

    compiler = Compiler(program)
    print(compiler.module)


if __name__ == "__main__":
    main()
