from enum import Enum


class AtomicLiteralKind(Enum):
    Int = 0
    Atom = 1
    NIl = 2
    CHAR = 3
    STRING = 4


class ConstantKind(Enum):
    ATOM = 0
    BRACE = 1
    BRACK = 2


class AtomicLiteral:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


class Constant:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


class FunctionName:
    def __init__(self, name, arg_num):
        self.name = name
        self, arg_num = arg_num
