# lllisp

lllisp is a lisp-like language that compiles to LLVM.

## Requirements

- Python 3.6
- `llvmlite`

## Installation

First off, install Python 3.6 by following the many guides available online and
on python.org; then install all the required packages by running `python3.6 -m
pip install -r --user requirements.txt`

## Usage

Create a file that contains some lllisp code, and name it whatever you want.
For the sake of this example, we'll assume your file is named `example.cl`.

To compile your code to LLVM IR, you just simply write at the command prompt:
```shell
python3 -m lllisp example.cl
```

Actually running/compiling will be added later. :+1:

## Reasoning

I've recently learned how to use LLVM and as many of you know when you have a
hammer everything looks like a nail. I thought it'd be pretty funny to write a
language that compiles to LLVM, but I'm *really* inexperienced with parsers so
I thought I'd write a language where parsing was really easy.
