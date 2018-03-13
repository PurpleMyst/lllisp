#!/usr/bin/env python3
import collections

import llvmlite.ir

from .objects import Symbol, Number, String, SExpr, LLVM_TYPES, BuiltinFunction
from .prelude import prelude


class Compiler:
    def __init__(self, s_exprs):
        self.module = llvmlite.ir.Module(name="lllisp")

        main_type = llvmlite.ir.FunctionType(llvmlite.ir.IntType(32), ())
        main_func = llvmlite.ir.Function(self.module, main_type, "main")
        entry = main_func.append_basic_block(name="entry")
        self.builder = llvmlite.ir.IRBuilder(entry)

        self.functions = collections.ChainMap({"main": main_func})
        self.variables = collections.ChainMap(prelude).new_child()

        rv = self._chain(s_exprs)
        if rv is not None:
            self.builder.ret(rv)
        else:
            self.builder.ret(main_type.return_type(0))

    @staticmethod
    def _random_name(size=10):
        import random
        import string

        return "".join(random.choice(string.ascii_letters)
                       for _ in range(size))

    def _chain(self, body):
        result = None

        if not hasattr(body, "__iter__"):
            body = SExpr.singleton(body)

        for value in body:
            result = self._compile_value(value)

        return result

    @staticmethod
    def _make_constant(llvm_type, value):
        # Make a constant from a lllisp value.
        llvm_type = LLVM_TYPES[llvm_type.value]
        return llvm_type(value.value)

    def _set_variable(self, name, value):
        # Assign a variable `name` to a value `value`. If a variable `name`
        # does not exist, create it in the current scope.
        if isinstance(name, Symbol):
            name = name.value

        if name not in self.variables:
            value = self._compile_value(value)
            llvm_type = value.type
            variable = self.builder.alloca(llvm_type)
            self.variables[name] = variable

        variable = self.variables[name]
        self.builder.store(value, variable)
        return variable

    def _load_variable(self, name):
        if isinstance(name, Symbol):
            name = name.value

        location = self.variables[name]

        if isinstance(location, llvmlite.ir.types.PointerType):
            return self.builder.load(location)
        else:
            # i.e. function arguments
            return location

    def _create_function(self, returntype, name, args, *body):
        # Create a `returntype name(args) { body }` function in the top-level
        # and return its `llvmlite.ir.Function` object.

        # TODO: Support closures. I'm not really sure how.
        self.variables = self.variables.new_child()

        returntype = LLVM_TYPES[returntype.value]

        llvm_argtypes = [LLVM_TYPES[ty.value] for (ty, _) in args]
        func_type = llvmlite.ir.FunctionType(returntype, llvm_argtypes)
        function = llvmlite.ir.Function(self.module, func_type, name.value)
        entry = function.append_basic_block(name="entry")

        for arg, (_, name) in zip(function.args, args):
            self.variables[name.value] = arg

        with self.builder.goto_block(entry):
            self.functions[name.value] = function

            rv = self._chain(body)
            if rv is not None:
                self.builder.ret(rv)

        self.variables = self.variables.parents
        return function

    def _compile_value(self, value):
        if isinstance(value, SExpr):
            name, *args = value

            if name.value == "defun":
                function = self._create_function(*args)
                self._set_variable(args[1], function)
            elif name.value == "setq":
                self._set_variable(*args)
            elif name.value == "begin":
                return self._chain(args)
            elif name.value == "constant":
                return self._make_constant(*args)
            elif name.value in self.variables:
                func = self.variables[name.value]

                if isinstance(func, BuiltinFunction):
                    # TODO: Verify returntype/args.
                    result = func.func(self, *args)
                    return result
                else:
                    # we're assuming this is a function
                    # TODO: don't assume
                    func = self.builder.load(func)
                    func_args = [self._compile_value(arg) for arg in args]
                    return self.builder.call(func, func_args)
            else:
                raise NameError(f"Unknown function {name.value!r}")
        elif isinstance(value, String):
            char = llvmlite.ir.IntType(8)
            s = bytearray(value.value.encode("utf8", "strict"))
            ty = llvmlite.ir.ArrayType(char,
                                       len(s))

            global_var = llvmlite.ir.GlobalVariable(self.module, ty,
                                                    self._random_name())
            global_var.initializer = ty(s)
            return self.builder.bitcast(global_var, char.as_pointer())
        elif isinstance(value, Number):
            raise RuntimeError("Please specify a type for your number. "
                               "For example, if you wanted an int, you could"
                               f"write `(constant int {value.value})`")
        elif isinstance(value, Symbol):
            return self._load_variable(value)
        elif isinstance(value, llvmlite.ir.values.Function):
            return value
        else:
            # TODO: Stuff.
            raise TypeError(type(value))
