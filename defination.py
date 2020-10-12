from enum import Enum

#
#   enum classes
#


class AtomicLiteralKind(Enum):
    INT = 0
    ATOM = 1
    NIL = 2
    CHAR = 3
    STRING = 4


class SingleExpressionKind(Enum):
    ATOMICLITERAL = 0
    VARNAME = 1
    FUNCTIONNAME = 2
    TUPLE = 3
    LIST = 4
    LET = 5
    CASE = 6
    FUN = 7
    APPLICATION = 8
    RECEIVE = 9
    CALL = 10
    SEQ = 11
    PRIMOP = 12


class ExpressionKind(Enum):
    SINGLE = 0
    VALUELIST = 1

#
#   difinations
#


class Expression:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


class AtomicLiteral:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


class SingleExpression:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = kind


class Call:
    def __init__(self, exp1, exp2, exps):
        self.exp1 = exp1
        self.exp2 = exp2
        self.exps = exps


class FunctionName:
    def __init__(self, name, arg_num, lineno):
        self.name = name
        self.arg_num = arg_num
        self.lineno = lineno


class FunctionDefine:
    def __init__(self, functionname):
        self.function_name = functionname


class Variable:
    def __init__(self, name, value, coverable):
        self.name = name
        self.value = value
        self.coverable = coverable


class GlobalVarTable:
    def __init__(self):
        self.cur_var_table = {}
        self.var_table_stack = []

    def begin_scope(self):
        new_var_table = {}
        for k, v in self.cur_var_table.items():
            new_var_table[k] = Variable(v.name, v.value, True)
        self.var_table_stack.append(self.cur_var_table)
        self.cur_var_table = new_var_table

    def end_scope(self):
        self.cur_var_table = self.var_table_stack.pop()

#
#   global variables
#


local_functions = []
gvt = GlobalVarTable()

#
#   global methods
#


def do_expression(expression):
    pass
