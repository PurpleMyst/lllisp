#!/usr/bin/env python3


prelude = {}


def define_builtin(name, llvm_type):
    def _inner(func):
        func.__name__ = name
        func.llvm_type = llvm_type
        prelude[name] = func
        return func
    return _inner
