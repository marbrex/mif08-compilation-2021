# Visitor to *interpret* MiniC files
from typing import Dict, List
import typing
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Errors import MiniCRuntimeError, MiniCInternalError

MINIC_VALUE = typing.Union[int, str, bool, float, List['MINIC_VALUE']]


class MiniCInterpretVisitor(MiniCVisitor):

    _memory: Dict[str, MINIC_VALUE]

    def __init__(self):
        self._memory = dict()  # store all variable ids and values.
        self.has_main = False

    # visitors for variable declarations

    # Reminder:
    # 'self' this pointer, 'ctx' stands for context

    def visitVarDecl(self, ctx) -> None:
        # Initialise all variables in self._memory
        # raise NotImplementedError()
        id_list = self.visit(ctx.id_l())
        for id_str in id_list:
            type_str = ctx.typee().getText()
            # print("id: " + id_str)
            # print("type_str: " + type_str)
            
            default_value = 0
            if type_str == "float":
                default_value = 0.0
            elif type_str == "bool":
                default_value = False
            elif type_str == "string":
                default_value = ""

            self._memory.update({id_str:default_value})
            # print(self._memory.get(id_str))

    def visitIdList(self, ctx) -> List[str]:
        # raise NotImplementedError()
        first_id = ctx.ID().getText()
        id_list = self.visit(ctx.id_l())
        id_list.append(first_id)
        return id_list
        

    def visitIdListBase(self, ctx) -> List[str]:
        return [ctx.ID().getText()]

    # visitors for atoms --> value

    def visitParExpr(self, ctx) -> MINIC_VALUE:
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx) -> int:
        return int(ctx.getText())

    def visitFloatAtom(self, ctx) -> float:
        return float(ctx.getText())

    def visitBooleanAtom(self, ctx) -> bool:
        return ctx.getText() == "true"

    def visitIdAtom(self, ctx) -> MINIC_VALUE:
        # raise NotImplementedError()
        return self._memory[ctx.ID().getText()]

    def visitStringAtom(self, ctx) -> str:
        return ctx.getText()[1:-1]

    # visit expressions

    def visitAtomExpr(self, ctx) -> MINIC_VALUE:
        return self.visit(ctx.atom())

    def visitOrExpr(self, ctx) -> bool:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        return lval | rval

    def visitAndExpr(self, ctx) -> bool:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        return lval & rval

    def visitEqualityExpr(self, ctx) -> bool:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        # be careful for float equality
        if ctx.myop.type == MiniCParser.EQ:
            return lval == rval
        else:
            return lval != rval

    def visitRelationalExpr(self, ctx) -> bool:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.LT:
            return lval < rval
        elif ctx.myop.type == MiniCParser.LTEQ:
            return lval <= rval
        elif ctx.myop.type == MiniCParser.GT:
            return lval > rval
        elif ctx.myop.type == MiniCParser.GTEQ:
            return lval >= rval
        else:
            raise MiniCInternalError(
                "Unknown comparison operator '%s'" % ctx.myop
            )

    def visitAdditiveExpr(self, ctx) -> MINIC_VALUE:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.PLUS:
            if any(isinstance(x, str) for x in (lval, rval)):
                return '{}{}'.format(lval, rval)
            else:
                return lval + rval
        elif ctx.myop.type == MiniCParser.MINUS:
            return lval - rval
        else:
            raise MiniCInternalError(
                "Unknown additive operator '%s'" % ctx.myop)

    def visitMultiplicativeExpr(self, ctx) -> MINIC_VALUE:
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.MULT:
            return lval * rval
        elif ctx.myop.type == MiniCParser.DIV:
            if rval == 0:
                raise MiniCRuntimeError("Division by 0")
            if isinstance(lval, int):
                return lval // rval
            else:
                return lval / rval
        elif ctx.myop.type == MiniCParser.MOD:
            # TODO : interpret modulo
            # raise NotImplementedError()
            # print("IN MODULO!")
            if rval == 0:
                raise MiniCRuntimeError("Division by 0")
            else:
                acc = 0
                while acc+rval <= lval:
                    acc += rval
                return lval - acc
        else:
            raise MiniCInternalError(
                "Unknown multiplicative operator '%s'" % ctx.myop)

    def visitNotExpr(self, ctx) -> bool:
        return not self.visit(ctx.expr())

    def visitUnaryMinusExpr(self, ctx) -> MINIC_VALUE:
        return -self.visit(ctx.expr())

    # visit statements

    def visitPrintlnintStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        if isinstance(val, bool):
            val = '1' if val else '0'
        print(val)

    def visitPrintlnfloatStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        if isinstance(val, float):
            val = "%.2f" % val
        print(val)

    def visitPrintlnstringStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        print(val)

    def visitAssignStat(self, ctx) -> None:
        # raise NotImplementedError()
        id_str = ctx.ID().getText()
        expr_val = self.visit(ctx.expr())
        self._memory.update({id_str:expr_val})
        # print(id_str)
        # print(expr_val)

    def visitIfStat(self, ctx) -> None:
        # raise NotImplementedError()
        expr_val = self.visit(ctx.expr())
        # print(expr_val)
        if expr_val:
            if_block = self.visit(ctx.stat_block(0))
            # print(if_block)
        elif ctx.ELSE() is not None:
            else_block = self.visit(ctx.stat_block(1))
            # print(else_block)

    def visitWhileStat(self, ctx) -> None:
        # raise NotImplementedError()
        expr_val = self.visit(ctx.expr())
        while expr_val:
            stat_block = self.visit(ctx.stat_block())
            expr_val = self.visit(ctx.expr())
            # print(expr_val)

    # TOPLEVEL
    def visitProgRule(self, ctx) -> None:
        self.visitChildren(ctx)
        if not self.has_main:
            # A program without a main function is compilable (hence
            # it's not a typing error per se), but not executable,
            # hence we consider it a runtime error.
            raise MiniCRuntimeError("No main function in file")

    # Visit a function: ignore if non main!
    def visitFuncDecl(self, ctx) -> None:
        funname = ctx.ID().getText()
        if funname == "main":
            self.has_main = True
            self.visit(ctx.vardecl_l())
            self.visit(ctx.block())
