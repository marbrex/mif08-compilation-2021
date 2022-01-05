# MiniC Compiler 
LAB4 (simple code generation), MIF08 / CAP 2021-22

# Authors

Eldar Kasmamytov (p1712650)

# Contents

In this lab, we generate low-level RISCV instructions (3-address assembly code) for the MiniC language from the source code.

# Howto

`python3 MiniCC.py TP04/tests/provided/step1/test00.c --reg-alloc=naive`: launch the compiler and obtain a RISCV code with temp.

`make TEST_FILES="TP04/tests/provided/step1/*.c" tests-naive`: check expected and compile with the naive allocation.

`make TEST_FILES="TP04/tests/provided/step1/*.c" tests-notsmart`: check expected and compile with the naive allocation and the all in memory allocation.

# Test design 

Tests inherit the same structure of the previous labs.
But in addition, a new annotation that lets to skip tests is used in this lab.

- 100% of code cover in MiniCCodeGen3AVisitor.py.
- Almost fully covered SimpleAllocations.py. The only part that is not being tested is "AllocationError" exception
in the "AllInMemAllocator".

# Design choices

Log prints are still in the code, but only shown if the "debug" option is specified on program execution.

Each functionality asked has been implemented and tested with care :)

# Known bugs

There are no known bugs.

# Checklists

A check ([X]) means that the feature is implemented 
and *tested* with appropriate test cases.

## Code generation

- [X] Number Atom 
- [X] Boolean Atom
- [X] Id Atom 
- [X] Additive expression
- [X] Multiplicative expr
- [X] UnaryMinus expr
- [X] Or expression
- [X] And expression
- [X] Equality expression
- [X] Relational expression (! many cases -> many tests)
- [X] Not expression

## Statements

- [X] Prog, assignements
- [X] While
- [X] Cond Block
- [X] If
- [X] Nested ifs
- [X] Nested whiles

## Allocation

- [X] Naive allocation
- [X] All in memory allocation
- [X] Massive tests of memory allocation

