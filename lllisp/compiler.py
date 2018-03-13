#!/usr/bin/env python3
import collections

import llvmlite.ir

from .parser import Symbol, Number, String, SExpr
from .prelude import prelude


LLVM_TYPES = {
    "int32": llvmlite.ir.IntType(32)
}


def compile_to_ir(toplevel_sexpr):
    module = llvmlite.ir.Module(name="lllisp")
    builder = llvmlite.ir.IRBuilder()

    functions = collections.ChainMap()
    variables = collections.ChainMap(prelude)

    depth = 0

    def chain(body):
        result = None

        if not isinstance(body, (SExpr, list)):
            body = SExpr.singleton(body)

        for value in body:
            result = compile_to_ir_impl(value)

        return result

    def compile_function(returntype, name, args, body):
        nonlocal depth

        returntype = LLVM_TYPES[returntype.value]

        # TODO: Add args
        assert not args
        llvm_type = llvmlite.ir.FunctionType(returntype, ())

        function = llvmlite.ir.Function(module, llvm_type, name.value)
        entry = function.append_basic_block(name="entry")
        builder.position_at_start(entry)

        functions[name.value] = function

        rv = compile_to_ir_impl(body)
        if rv is not None:
            builder.ret(rv)

    def define_variable(name, value):
        value = compile_to_ir_impl(value)
        llvm_type = value.type
        variable = builder.alloca(llvm_type)
        builder.store(value, variable)
        variables[name.value] = variable
        return variable

    def make_constant(llvm_type, value):
        llvm_type = LLVM_TYPES[llvm_type.value]
        return llvm_type(value.value)

    def compile_to_ir_impl(value):
        nonlocal depth

        if isinstance(value, SExpr):
            name, *args = value

            if name.value == "function":
                if depth == 0:
                    depth += 1
                    compile_function(*args)
                    depth -= 1
                else:
                    raise RuntimeError("Can not define function "
                                       "not at the top level.")
            elif name.value == "let":
                define_variable(*args)
            elif name.value == "begin":
                return chain(args)
            elif name.value == "constant":
                return make_constant(*args)
            else:
                # TODO: Look stuff up in prelude.
                raise NameError(f"Unknown function {name.value!r}")
        elif isinstance(value, (String, Number)):
            return value
        elif isinstance(value, Symbol):
            return builder.load(variables[value.value])
        else:
            # TODO: Stuff.
            raise TypeError(type(value))

    for sexpr in toplevel_sexpr:
        compile_to_ir_impl(sexpr)

    return module
