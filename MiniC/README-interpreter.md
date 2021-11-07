# MiniC interpreter and typer
LAB3, MIF08 / CAP 2021-22


# Authors

KASMAMYTOV ELDAR (p1712650)

# Contents

Once the static parts, that are Lexing and Parsing are successfuly completed and finished, we are going to proceed to the dynamic part, which is interpreting the language. For this the Visitor design pattern is being used, that applies different behaviour for each expresssion and statement based on their context and/or type.

**All functionalities** are **implemented** and **work fine**, they have been **tested with both provided and custom test sets**.

# Howto

`make tests-interpret TEST_FILES='TP03/tests/provided/examples/test00.c'` for a single run
it should print 42

`make tests` to test all the files in `*/tests/*` according to `EXPECTED` results.

You can select the files you want to test by using `make tests TEST_FILES='TP03/**/*bad*.c'` (`**` means
"any number of possibly nested directories").

# Test design 

During implementation of the functionalities, **many tests** have been created to test new features **step by step**. You can find both **positive and negative** custom tests in the 'tests/students' directory.

# Design choices

Each functionality asked has been implemented and tested with care :)

# Known bugs

There are no any known bugs. Every noticed bug has been fixed.
