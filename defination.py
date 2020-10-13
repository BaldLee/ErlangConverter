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
    def __init__(self, kind: ExpressionKind, value):
        self.kind = kind
        self.value = value


class AtomicLiteral:
    def __init__(self, kind: AtomicLiteralKind, value):
        self.kind = kind
        self.value = value


class SingleExpression:
    def __init__(self, kind: SingleExpressionKind, value):
        self.kind = kind
        self.value = value


class Call:
    def __init__(self, exp1: Expression, exp2: Expression, exps: list[Expression]):
        self.exp1 = exp1
        self.exp2 = exp2
        self.exps = exps


class Application:
    def __init__(self, exp: Expression, exps: list[Expression]):
        self.exp = exp
        self.exps = exps


class Let:
    def __init__(self, varname, exp1: Expression, exp2: Expression):
        self.varname = varname
        self.exp1 = exp1
        self.exp2 = exp2


class Clause:
    def __init__(self, pattern, guard, exp: Expression):
        self.pattern = pattern
        self.guard = guard
        self.exp = exp


class Case:
    def __init__(self, exp: Expression, clauses: list[Clause]):
        self.exp = exp
        self.clauses = clauses


class FunctionName:
    def __init__(self, name, arg_num, lineno):
        self.name = name
        self.arg_num = arg_num
        self.lineno = lineno


class FunctionDefine:
    def __init__(self, functionname, fun):
        self.function_name = functionname
        self.fun = fun


class Fun:
    def __init__(self, varnames, exp: Expression):
        self.varnames = varnames
        self.exp = exp


class Receive:
    def __init__(self, clauses: list[Clause]):
        self.clauses = clauses


class Sequencing:
    def __init__(self, exp1: Expression, exp2: Expression):
        self.exp1 = exp1
        self.exp2 = exp2


class GlobalVarTable:
    def __init__(self):
        self.cur_var_table = {}
        self.var_table_stack = []

    def begin_scope(self):
        new_var_table = {}
        for k, v in self.cur_var_table.items():
            new_var_table[k] = v.value
        self.var_table_stack.append(self.cur_var_table)
        self.cur_var_table = new_var_table

    def end_scope(self):
        self.cur_var_table = self.var_table_stack.pop()

#
#   global variables
#


local_functions = {}
gvt = GlobalVarTable()

#
#   global methods
#


def do_expression(expression: Expression):
    if expression.kind == ExpressionKind.SINGLE:
        do_single(expression.value)
    elif expression.kind == ExpressionKind.VALUELIST:
        do_value_list(expression.value)


def do_value_list(vl: list[SingleExpression]):
    for item in vl:
        do_single(item)


def do_single(s: SingleExpression):
    if s.kind == SingleExpressionKind.ATOMICLITERAL:
        pass  # do nothing
    elif s.kind == SingleExpressionKind.VARNAME:
        do_expression(gvt.cur_var_table[s.value].value)
    elif s.kind == SingleExpressionKind.FUNCTIONNAME:
        pass  # do nothing
    elif s.kind == SingleExpressionKind.TUPLE:
        pass  # wait
    elif s.kind == SingleExpressionKind.LIST:
        pass  # wait
    elif s.kind == SingleExpressionKind.LET:
        let = s.value
        gvt.begin_scope()
        gvt.cur_var_table[let.varname] = let.exp1
        do_expression(let.exp2)
        gvt.end_scope()
    elif s.kind == SingleExpressionKind.CASE:  # not finish
        clauses = s.value.clauses
        for item in clauses:
            do_expression(item.exp)
    elif s.kind == SingleExpressionKind.FUN:
        # gvt.begin_scope()
        do_expression(s.value.exp)
        # gvt.end_scope()
    elif s.kind == SingleExpressionKind.APPLICATION:
        apply = s.value
        gvt.begin_scope()
        if apply.exp.kind != ExpressionKind.SINGLE:
            print("#error: application's exp should be single")
        elif apply.exp.value.kind != SingleExpressionKind.FUNCTIONNAME:
            print("#error: application's exp should be functionname")
        else:
            fun = local_functions[apply.exp.value.value.name]
            for i in range(len(fun.varnames)):
                gvt.cur_var_table[fun.varnames[i]] = apply.exps[i]
            do_expression(fun.exp)
        gvt.end_scope()
    elif s.kind == SingleExpressionKind.RECEIVE:  # not finish
        clauses = s.value.clauses
        for item in clauses:
            do_expression(item.exp)
    elif s.kind == SingleExpressionKind.CALL:
        # check exp1 and exp2
        # do'erlang':'!' and 'erlang':'spawn'
        pass
    elif s.kind == SingleExpressionKind.SEQ:
        seq = s.value
        do_expression(seq.exp1)
        do_expression(seq.exp2)
    elif s.kind == SingleExpression.PRIMOP:
        pass  # DO NOTHING
    else:
        print("#error unknown type single expression")
