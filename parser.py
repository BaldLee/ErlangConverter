import ply.lex as lex
import ply.yacc as yacc
from defination import *

#
#
#           Lex Analysis
#
#

reserved = {
    'after': 'AFTER',
    'apply': 'APPLAY',
    'attributes': 'ATTRIBUTES',
    'call': 'CALL',
    'case': 'CASE',
    'catch': 'CATCH',
    'do': 'DO',
    'end': 'END',
    'fun': 'FUN',
    'in': 'IN',
    'let': 'LET',
    'letrec': 'LETREC',
    'module': 'MODEULE',
    'of': 'OF',
    'primop': 'PRIMOP',
    'receive': 'RECEIVE',
    'try': 'TRY',
    'when': 'WHEN'
}

tokens = [
    'ATOM',
    'CHAR',
    'STRING',
    'VARNAME',
    'NUMBER',
    'COMMENT',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',
    'LABRACK',
    'RABRACK',
    'VBAR',
    'NSIGN',
    'COMMA',
    'COLON',
    'SLASH',
    'EQUAL',
    'ARROW',
    'ANNOTATION',
    'PLUS',
    'MINUS',
    'MULTI',
    'EXCLAIM',
    'APO'
] + list(reserved.values())

t_ATOM = r'\'[A-Za-z0-9_@\s]*\''
t_CHAR = r'\$[A-Za-z0-9_@]'
t_STRING = r'\"[A-Za-z0-9_@\s]*\"'
t_VARNAME = r'[A-Z_][A-Za-z0-9@_]*'


def t_NUMBER(t):  # numbers
    r'\d+'
    t.value = int(t.value)
    return t


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LABRACK = r'<'
t_RABRACK = r'>'
t_VBAR = r'\|'
t_NSIGN = r'#'
t_COMMA = r','
t_COLON = r':'
t_SLASH = r'/'
t_EQUAL = r'='
t_ARROW = r'->'
t_ANNOTATION = r'-\|'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTI = r'\*'
t_EXCLAIM = r'\!'
t_APO = r'\''

t_ignore = ' \t'  # Ignore tokens


def t_newline(t):  # Newline token
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):  # No return value. Token discarded
    r'%%.*'
    pass


def t_error(t):  # Error handler
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# init lexer
lexer = lex.lex()

data = ''''''

lexer.input(data)
for token in lexer:
    print(token)

#
#
#         Grammar Analysis
#
#


# Atomic literal: integer, atom, nil, char and string
def p_atomliteral_int(p):
    'atomliteral : NUMBER'
    p[0] = AtomicLiteral(AtomicLiteralKind.INT, p[1])


def p_atomliteral_atom(p):
    'atomliteral : ATOM'
    p[0] = AtomicLiteral(AtomicLiteralKind.ATOM, p[1])


def p_atomliteral_nil(p):
    'atomliteral : nil'
    p[0] = AtomicLiteral(AtomicLiteralKind.NIL, p[1])


def p_atomliteral_char(p):
    'atomliteral : CHAR'
    p[0] = AtomicLiteral(AtomicLiteralKind.CHAR, p[1])


def p_atomliteral_string(p):
    'atomliteral : STRING'
    p[0] = AtomicLiteral(AtomicLiteralKind.STRING, p[1])


def p_nil(p):
    # Nil : []
    'nil : LBRACK RBRACK'
    p[0] = []


# constant: atomic literal, { } , {...} , [...] and [...|.]
def p_constant_atom(p):
    'constant : atomliteral'
    p[0] = Constant(ConstantKind.ATOM, p[1])


def p_constant_bracenone(p):
    'constant : LBRACE RBRACE'
    p[0] = Constant(ConstantKind.BRACE, None)


def p_constant_brace(p):
    'constant : LBRACE constants RBRACE'
    p[0] = Constant(ConstantKind.BRACE, p[2])


def p_constant_brack(p):
    'constant : LBRACK constants RBRACK'
    p[0] = Constant(ConstantKind.BRACK, p[2])


def p_constant_brackvbar(p):
    'constant : LBRACK constants VBAR constant RBRACK'
    p[0] = Constant(ConstantKind.BRACK, p[2].append(p[4]))


def p_constants_one(p):
    'constants : constant'
    p[0] = []
    p[0].append(p[1])


def p_constants_combine(p):
    'constants : constants COMMA constant'
    p[0] = p[1]
    p[0].append(p[3])


def p_module(p):
    'module : MODULE ATOM moduleheader modulebody END'
    # wait
    pass


def p_moduleheader(p):
    'moduleheader : exports attributes'
    # wait
    pass


def p_exports(p):
    'exports : LBARCK functionnames RBRACK'
    # wait
    pass


def p_functionname(p):
    'functionname : ATOM SLASH NUMBER'
    p[0] = FunstionName(p[1], p[3])


def p_functionnames_one(p):
    'functionnames : functionname'
    p[0] = []
    p[0].append(p[1])


def p_functionnames_combine(p):
    'functionnames : functionnames COMMA functionname'
    p[0] = p[1]
    p[0].append(p[3])


def p_attributes(p):
    'attributes : ATTRIBUTES LBRACK moduleattributes RBRACK'
    # wait
    pass


def p_moduleattribute(p):
    'moduleattribute : ATOM EQUAL CONSTANT'
    # wait
    pass


def p_moduleattributes_one(p):
    'moduleattributes : moduleattribute'
    # wait
    pass


def p_moduleattributes_combine(p):
    'moduleattributes : moduleattributes COMMA moduleattribute'
    # wait
    pass


def p_modulebody(p):
    'modulebody : functiondefines'
    # wait
    pass


def p_functiondefines_one(p):
    'functiondefines : functiondefine'
    # wait
    pass


def p_functiondefines_combine(p):
    'functiondefines : functiondefines functiondefine'
    # wait
    pass


def p_functiondefine(p):
    'functiondefine : afunctionname = afun'
    # wait
    pass


def p_afunctionname_notannotated(p):
    'afunctionname : functionname'
    p[0] = p[1]


def p_afunctionname_annotated(p):
    'afunctionname : LPAREN functionname ANNOTATION LBRACK constants RBACK RPAREN'
    p[0] = p[2]


def p_afun_notannotated(p):
    'afun : fun'
    p[0] = p[1]


def p_afun_annotated(p):
    'afun : LPAREN fun ANNOTATION LBRACK constants RBRACK RPAREN'
    p[0] = p[2]


def p_expression_vlist(p):
    'expression : valuelist'
    pass  # wait


def p_expression_singleexpression(p):
    'expression : singleexpression'
    pass  # wait


def p_valuelist(p):
    'valuelist : LABRACK singleexpressions RABRACK'
    pass  # wait


def p_singleexpressions_one(p):
    'singleexpressions : singleexpression'
    pass  # wait


def p_singleexpressions_combine(p):
    'singleexpressions : singleexpressions COMMA singleexpression'
    pass  # wait


def p_singleexpression_atomicliteral(p):
    'singleexpression : atomliteral'
    pass  # wait


def p_singleexpression_varname(p):
    'singleexpression : VARNAME'
    pass  # wait


def p_singleexpression_functionname(p):
    'singleexpression : functionname'
    pass  # wait


def p_singleexpression_tuple(p):
    'singleexpression : tuple'
    pass  # wait


def p_singleexpression_list(p):
    'singleexpression : list'
    pass  # wait


def p_singleexpression_let(p):
    'singleexpression : let'
    pass  # wait


def p_singleexpression_case(p):
    'singleexpression : case'
    pass  # wait


def p_singleexpression_fun(p):
    'singleexpression : fun'
    pass  # wait


def p_singleexpression_application(p):
    'singleexpression : application'
    pass  # wait


def p_singleexpression_receive(p):
    'singleexpression : receive'
    pass  # wait


def p_var_varname(p):
    'var : VARNAME'
    pass  # wait


def p_var_varlist(p):
    'var : LRBRACK varnames RABRACK'
    pass  # wait

def p_var_empty(p):
    'var : LRABRACK RABRACK'
    pass # wait