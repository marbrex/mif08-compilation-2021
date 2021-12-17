from typing import List, Tuple
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from .APIRiscV import (LinearCode, Condition)
from . import Operands
from antlr4.tree.Trees import Parser, Trees
from Errors import MiniCInternalError, MiniCUnsupportedError

"""
CAP, MIF08, three-address code generation + simple alloc
This visitor constructs an object of type "LinearCode".
"""


class MiniCCodeGen3AVisitor(MiniCVisitor):

    _current_function: LinearCode

    def __init__(self, debug, parser):
        super().__init__()
        self._parser = parser
        self._debug = debug
        self._functions = []
        self._lastlabel = ""

    def get_functions(self):
        return self._functions

    def printSymbolTable(self):  # pragma: no cover
        print("--variables to temporaries map--")
        for keys, values in self._symbol_table.items():
            print(keys + '-->' + str(values))

    # handle variable decl

    def visitVarDecl(self, ctx) -> None:
        type_str = ctx.typee().getText()
        vars_l = self.visit(ctx.id_l())
        for name in vars_l:
            if name in self._symbol_table:
                raise MiniCInternalError(
                    "Variable {} has already been declared".format(name))
            else:
                tmp = self._current_function.new_tmp()
                self._symbol_table[name] = tmp
                if type_str not in ("int", "bool"):
                    raise MiniCUnsupportedError("Unsupported type " + type_str)
                # Initialization to 0 or False, both represented with 0
                self._current_function.add_instruction_LI(tmp, 0)

    def visitIdList(self, ctx) -> Operands.Temporary:
        t = self.visit(ctx.id_l())
        t.append(ctx.ID().getText())
        return t

    def visitIdListBase(self, ctx) -> List[str]:
        return [ctx.ID().getText()]

    # expressions

    def visitParExpr(self, ctx) -> Operands.Temporary:
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx) -> Operands.Temporary:
        val = int(ctx.getText())
        dest_temp = self._current_function.new_tmp()
        self._current_function.add_instruction_LI(dest_temp, val)
        return dest_temp

    def visitFloatAtom(self, ctx) -> Operands.Temporary:
        raise MiniCUnsupportedError("float literal")

    def visitBooleanAtom(self, ctx) -> Operands.Temporary:
        # raise NotImplementedError() # TODO (Exercise 5)
        # true is 1 false is 0
        val = 1 if ctx.getText() == "true" else 0
        dest_temp = self._current_function.new_tmp()
        self._current_function.add_instruction_LI(dest_temp, val)
        return dest_temp

    def visitIdAtom(self, ctx) -> Operands.Temporary:
        try:
            # get the temporary associated to id
            return self._symbol_table[ctx.getText()]
        except KeyError:  # pragma: no cover
            raise MiniCInternalError(
                "Undefined variable {}, this should have failed to typecheck."
                .format(ctx.getText())
            )

    def visitStringAtom(self, ctx) -> Operands.Temporary:
        raise MiniCUnsupportedError("string atom")

    # now visit expressions

    def visitAtomExpr(self, ctx) -> Operands.Temporary:
        return self.visit(ctx.atom())

    def visitAdditiveExpr(self, ctx) -> Operands.Temporary:
        # raise NotImplementedError() # TODO (Exercise 2)
        # Here ctx.expr() returns an Array with 2 expressions
        exprs = ctx.expr()
        if self._debug:
            print("visitAdditiveExpr: ")
            print("exprs: ", exprs)
        temp_left = self.visit(exprs[0])
        temp_right = self.visit(exprs[1])
        temp_dest = self._current_function.new_tmp()
        if self._debug:
            print(temp_left.get_alloced_loc()) # returns a String of form "temp_{n}"
            print(temp_right.get_alloced_loc())
        if ctx.myop.type == MiniCParser.PLUS:
            if self._debug:
                print("action: plus")
            self._current_function.add_instruction_ADD(temp_dest, temp_left, temp_right)
        elif ctx.myop.type == MiniCParser.MINUS:
            if self._debug:
                print("action: minus")
            self._current_function.add_instruction_SUB(temp_dest, temp_left, temp_right)
        return temp_dest

    def visitOrExpr(self, ctx) -> Operands.Temporary:
        # raise NotImplementedError() # TODO (Exercise 2)
        exprs = ctx.expr()
        if self._debug:
            print("visitOrExpr: ")
            print("exprs: ", exprs)
        temp_left = self.visit(exprs[0])
        temp_right = self.visit(exprs[1])
        temp_dest = self._current_function.new_tmp()
        self._current_function.add_instruction_OR(temp_dest, temp_left, temp_right)
        return temp_dest

    def visitAndExpr(self, ctx) -> Operands.Temporary:
        # raise NotImplementedError() # TODO (Exercise 2)
        exprs = ctx.expr()
        if self._debug:
            print("visitAndExpr: ")
            print("exprs: ", exprs)
        temp_left = self.visit(exprs[0])
        temp_right = self.visit(exprs[1])
        temp_dest = self._current_function.new_tmp()
        self._current_function.add_instruction_AND(temp_dest, temp_left, temp_right)
        return temp_dest

    def visitEqualityExpr(self, ctx) -> Operands.Temporary:
        return self.visitRelationalExpr(ctx)

    def visitRelationalExpr(self, ctx) -> Operands.Temporary:
        # raise NotImplementedError() # TODO (Exercise 5)
        c = Condition(ctx.myop.type)
        exprs = ctx.expr()
        temp_left = self.visit(exprs[0])
        temp_right = self.visit(exprs[1])
        temp_dest = self._current_function.new_tmp()
        rel_expr_false_label = self._current_function.new_label("rel_expr_false")
        rel_expr_end_label = self._current_function.new_label("rel_expr_end")
        if self._debug:
            print("relational expression:")
            print(Trees.toStringTree(ctx, None, self._parser))
            print("Condition: ", c)
            print("exprs: ", exprs)
            print("left_expr: ", Trees.toStringTree(exprs[0], None, self._parser))
            print("right_expr: ", Trees.toStringTree(exprs[1], None, self._parser))
        self._current_function.add_instruction_cond_JUMP(rel_expr_false_label, temp_left, c.negate(), temp_right)
        self._current_function.add_instruction_LI(temp_dest, 1)
        self._current_function.add_instruction_JUMP(rel_expr_end_label)
        self._current_function.add_label(rel_expr_false_label)
        self._current_function.add_instruction_LI(temp_dest, 0)
        self._current_function.add_label(rel_expr_end_label)
        return temp_dest

    def visitMultiplicativeExpr(self, ctx) -> Operands.Temporary:
        div_by_zero_lbl = self._current_function.get_label_div_by_zero()
        # raise NotImplementedError() # TODO (Exercise 2 or at the end)
        exprs = ctx.expr()
        if self._debug:
            print("visitMultiplicativeExpr: ")
            print(exprs)
        temp_left = self.visit(exprs[0])
        temp_right = self.visit(exprs[1])
        temp_dest = self._current_function.new_tmp()
        if self._debug:
            print(temp_left.get_alloced_loc()) # returns a String of form "temp_{n}"
            print(temp_right.get_alloced_loc())
        if ctx.myop.type == MiniCParser.MULT:
            if self._debug:
                print("multiplication")
                print(type(temp_left))
                print(type(temp_right))
            self._current_function.add_instruction_MUL(temp_dest, temp_left, temp_right)
        elif ctx.myop.type == MiniCParser.DIV:
            if self._debug:
                print("division")
                print(type(temp_left))
                print(type(temp_right))
            self._current_function.add_instruction_cond_JUMP(div_by_zero_lbl, temp_right, Condition("beq"), 0)
            self._current_function.add_instruction_DIV(temp_dest, temp_left, temp_right)
        elif ctx.myop.type == MiniCParser.MOD:
            if self._debug:
                print("modulo")
                print(type(temp_left))
                print(type(temp_right))
            self._current_function.add_instruction_cond_JUMP(div_by_zero_lbl, temp_right, Condition("beq"), 0)
            self._current_function.add_instruction_REM(temp_dest, temp_left, temp_right)
        return temp_dest

    def visitNotExpr(self, ctx) -> Operands.Temporary:
        # raise NotImplementedError() # TODO (Exercise 5)
        temp_expr = self.visit(ctx.expr())
        temp_dest = self._current_function.new_tmp()
        if self._debug:
            print("visitNotExpr:")
            print(ctx.expr())
            print(type(temp_expr))
            print(temp_expr)
            print(temp_expr.get_alloced_loc())
        self._current_function.add_instruction_NOT(temp_dest, temp_expr)
        return temp_dest

    def visitUnaryMinusExpr(self, ctx) -> Operands.Temporary:
        # raise NotImplementedError("unaryminusexpr") # TODO (Exercise 2)
        if self._debug:
            print("visitUnaryMinusExpr:")
        temp_expr = self.visit(ctx.expr())
        temp_dest = self._current_function.new_tmp()
        self._current_function.add_instruction_SUB(temp_dest, Operands.ZERO, temp_expr)
        return temp_dest

    def visitProgRule(self, ctx) -> None:
        self.visitChildren(ctx)

    def visitFuncDecl(self, ctx) -> None:
        funcname = ctx.ID().getText()
        self._current_function = LinearCode(funcname)
        self._symbol_table = dict()

        self.visit(ctx.vardecl_l())
        self.visit(ctx.block())
        self._current_function.add_comment("Return at end of function:")
        # This skeleton doesn't deal properly with functions, and
        # hardcodes a "return 0;" at the end of function. Generate
        # code for this "return 0;".
        self._current_function.add_instruction_LI(Operands.A0, 0)
        self._functions.append(self._current_function)
        del self._current_function

    def visitAssignStat(self, ctx) -> None:
        if self._debug:
            print("assign statement, rightexpression is:")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
        expr_temp = self.visit(ctx.expr())
        name = ctx.ID().getText()
        self._current_function.add_instruction_MV(self._symbol_table[name], expr_temp)

    def visitIfStat(self, ctx) -> None:
        expr = ctx.expr()
        blocks = ctx.stat_block()
        true_block = blocks[0]
        has_false_block = False
        false_block = None
        if len(blocks) > 1:
            has_false_block = True
            false_block = blocks[1]
        temp_expr = self.visit(expr)
        if self._debug:
            print("if statement")
            print("expr: ", expr)
            print("stat_block: ", blocks)
            print("true_block: ", true_block)
            if has_false_block:
                print("false_block: ", false_block)
            print("ctx.ELSE(): ", ctx.ELSE())
        if_false_label = self._current_function.new_label("if_false")
        end_if_label = self._current_function.new_label("end_if")
        # raise NotImplementedError() # TODO (Exercise 5)
        self._current_function.add_instruction_cond_JUMP(if_false_label, temp_expr, Condition(MiniCParser.EQ), 0)
        # EXECUTE IF TRUE BLOCK HERE
        self.visit(true_block)
        self._current_function.add_instruction_JUMP(end_if_label)
        if has_false_block:
            self._current_function.add_label(if_false_label)
            # EXECUTE IF FALSE BLOCK HERE
            self.visit(false_block)
        self._current_function.add_label(end_if_label)

    def visitWhileStat(self, ctx) -> None:
        expr = ctx.expr()
        stat = ctx.stat_block()
        temp_expr = self.visit(expr)
        if self._debug:
            print("while statement, condition is:")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
            print("and block is:")
            print(Trees.toStringTree(ctx.stat_block(), None, self._parser))
        while_cond_label = self._current_function.new_label("while_cond")
        while_end_label = self._current_function.new_label("while_end")
        # raise NotImplementedError() # TODO (Exercise 5)
        self._current_function.add_label(while_cond_label)
        temp_expr = self.visit(expr) # IMPORTANT: re-evaluate the while condition, otherwise infinite loop
        self._current_function.add_instruction_cond_JUMP(while_end_label, temp_expr, Condition(MiniCParser.EQ), 0)
        # EXECUTE WHILE BLOCK HERE
        self.visit(stat)
        self._current_function.add_instruction_JUMP(while_cond_label)
        self._current_function.add_label(while_end_label)

    def visitPrintlnintStat(self, ctx) -> None:
        expr_loc = self.visit(ctx.expr())
        if self._debug:
            print("print_int statement, expression is:")
            print(Trees.toStringTree(ctx.expr(), None, self._parser))
        self._current_function.add_instruction_PRINTLN_INT(expr_loc)

    def visitPrintlnfloatStat(self, ctx) -> None:
        raise MiniCUnsupportedError("Unsupported type float")

    def visitPrintlnstringStat(self, ctx) -> None:
        raise MiniCUnsupportedError("Unsupported type string")

    def visitStatList(self, ctx) -> None:
        for stat in ctx.stat():
            self._current_function.add_comment(Trees.toStringTree(stat, None, self._parser))
            self.visit(stat)
