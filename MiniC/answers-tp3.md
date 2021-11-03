# **Answers for TP3**

## **Exercise 4**

- **Q: How do we handle a multiplication between int and string operands?**\
A: In the base implementation of the MiniC Interpreter, the multiplication between int and string is not allowed.\
The program is terminated with the **exitcode 2**.\
An exemple of this is given in `/MiniC/TP03/tests/provided/examples-types/bad_type01.c`

- **Q: How do we handle an assignment between a variable and an expression with the “wrong” type?**\
A: Similarly, this type of assignment is not allowed.\
The program is terminated with the **exitcode 2**.\
An exemple of this is given in `/MiniC/TP03/tests/provided/examples-types/bad_type00.c`

- **Q: How do we remember the declared type for each variable?**\
A: 

## **Exercise 6**

| Expression | Interpretation (Evaluation) |
| :--------- | :-------------------------- |
| x := e     | `v <- e.visit()`<br>`store(x,v)` #update the value in dict |
| println_int(e) | `v <- e.visit()`<br>`print(v)` #python’s print |
| S1; S2 | `s1.visit()`<br>`s2.visit()` |
| if b then S1 else S2 | `ve <- b.visit()`<br>`if ve == true :`<br>`s1.visit()`<br>`else:`<br>`s2.visit()`<br>`endif` |
| while b do S done | `loop :`<br>`ve <- b.visit()`<br>`if ve == true :`<br>`s1.visit()`<br>`goto loop`<br>`endif` |
