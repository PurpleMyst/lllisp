#!/usr/bin/env python3
import llvmlite.ir

from .objects import BuiltinFunction, LLVM_TYPES

__all__ = ["prelude"]

prelude = {}


def define_builtin(name, returntype, args):
    args = []

    for i, arg in enumerate(args):
        if arg is Ellipsis:
            print("var_arg")
        else:
            args.append(LLVM_TYPES[arg])

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


@define_builtin("printf", "int", ("string", ...))
def _printf(compiler, fmt, *args):
    printf_args = [compiler._compile_value(fmt)]
    printf_args.extend(compiler._compile_value(arg) for arg in args)

    # TODO: Move these somewhere else.
    printf_type = llvmlite.ir.FunctionType(llvmlite.ir.IntType(32), (llvmlite.ir.IntType(8).as_pointer(),), var_arg=True)
    printf = llvmlite.ir.Function(compiler.module, printf_type, name="printf")

    compiler.builder.call(printf, printf_args)
