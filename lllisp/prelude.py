#!/usr/bin/env python3

from .objects import BuiltinFunction, LLVM_TYPES

__all__ = ["prelude"]

prelude = {}


def define_builtin(name, returntype, args):
    args = tuple(LLVM_TYPES[arg] for arg in args)
    def _inner(func):
        func.__name__ = name
        prelude[name] = BuiltinFunction(returntype, func, args)
        return func
    return _inner


# TODO: Support generic functions.
@define_builtin("+", "int", ("int", "int"))
def _plus(compiler, lhs, rhs):
    lhs = compiler._compile_value(lhs)
    rhs = compiler._compile_value(rhs)
    result = compiler.builder.add(lhs, rhs)
    return result
