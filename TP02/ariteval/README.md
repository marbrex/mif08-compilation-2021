# LAB2, arithmetic expressions interpreter
MIF08, 2020-2021, Laure Gonnord & Matthieu Moy

# Completed by
Eldar Kasmamytov p1712650

# Content

This directory contains an interpreter for simple arithmetic
expressions like 5+3, for instance. The intepreter evaluates the
arithmetic expressions and prints their value on the standard
output.

# Usage

* `make` to generate AritLexer.py and AritParser.py (once)

* `python3 arit1.py <path/and/test/name>` to test a given file, for
 instance: 
 `python3 arit1.py tests/test01.txt`  should print `1+2 = 3`

* `make tests` to test on all tests files of the `testfile` directory

# Syntax of our language/restrictions

The syntax is the one textually given in the Lab2 sheet. 
Restriction : we did not implement minus nor unary minus.

# Design choices

- Implemented **equally prioritized** Minus and Plus rules
- Unary Minus is ordered **at the top of the list as the most prioritized rule**
- Wrote **multiple tests** for the above mentioned rules.
- Added **Integer Division**, that has the **same priority order as the Mult. operator**

# Known bugs

- division by zero is accepted by the parser (pre-condition, it's up to the user to not divide by zero) and is handled by python, which throws an exception as the division by zero is impossible. No test, because there is no an expected value.
