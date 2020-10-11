import ply.lex as lex
import ply.yacc as yacc
from defination import *

#
#
#           Lex Analysis
#
#

# reserved = {
#     'after': 'AFTER',
#     'apply': 'APPLAY',
#     'attributes': 'ATTRIBUTES',
#     'call': 'CALL',
#     'case': 'CASE',
#     'catch': 'CATCH',
#     'do': 'DO',
#     'end': 'END',
#     'fun': 'FUN',
#     'in': 'IN',
#     'let': 'LET',
#     'letrec': 'LETREC',
#     'module': 'MODULE',
#     'of': 'OF',
#     'primop': 'PRIMOP',
#     'receive': 'RECEIVE',
#     'try': 'TRY',
#     'when': 'WHEN'
# }

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
    # 'NSIGN',
    'COMMA',
    'COLON',
    'SLASH',
    'EQUAL',
    'ARROW',
    'ANNOTATION',
    # 'PLUS',
    # 'MINUS',
    # 'MULTI',
    # 'EXCLAIM',
    # 'APO',
    'AFTER',
    'APPLY',
    'ATTRIBUTES',
    'CALL',
    'CASE',
    # 'CATCH',
    'DO',
    'END',
    'FUN',
    'IN',
    'LET',
    # 'LETREC',
    'MODULE',
    'OF',
    'PRIMOP',
    'RECEIVE',
    # 'TRY',
    'WHEN'
]

t_ATOM = r'\'[^\\^\']*\''
t_CHAR = r'\$[A-Za-z0-9_@]'
t_STRING = r'\"[A-Za-z0-9_@\s]*\"'
t_VARNAME = r'([A-Z]|_[A-Za-z0-9@_])[A-Za-z0-9@_]*'


# def t_VARNAME(t):
#     r'[A-Z_][A-Za-z0-9@_]*'
#     t.type = reserved.get(t.value, 'VARNAME')  # cheack reserved words
#     return t


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
# t_NSIGN = r'\#'
t_COMMA = r','
t_COLON = r':'
t_SLASH = r'/'
t_EQUAL = r'='
t_ARROW = r'->'
t_ANNOTATION = r'-\|'
# t_PLUS = r'\+'
# t_MINUS = r'-'
# t_MULTI = r'\*'
# t_EXCLAIM = r'\!'
# t_APO = r'\''
t_AFTER = r'after'
t_APPLY = r'apply'
t_ATTRIBUTES = r'attributes'
t_CALL = r'call'
t_CASE = r'case'
# t_CATCH = r'catch'
t_DO = r'do'
t_END = r'end'
t_FUN = r'fun'
t_IN = r'in'
t_LET = r'let'
# t_LETREC = r'letrec'
t_MODULE = r'module'
t_OF = r'of'
t_PRIMOP = r'primop'
t_RECEIVE = r'receive'
# t_TRY = r'try'
t_WHEN = r'when'


t_ignore = ' \t'  # Ignore tokens


def t_newline(t):  # Newline token
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):  # No return value. Token discarded
    r'%%.*'
    pass


def t_error(t):  # Error handler
    print("Illegal character '%s'. LINE %d " % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


# init lexer
lexer = lex.lex()

# data = ''''''
# lexer.input(data)
# for token in lexer:
#     print(token)

#
#
#         Grammar Analysis
#
#


def p_module(p):
    'module : MODULE ATOM moduleheader modulebody END'
    # wait
    print("done")
    pass


def p_moduleheader(p):
    'moduleheader : exports attributes'
    # wait
    pass


def p_exports(p):
    'exports : LBRACK functionnames RBRACK'
    # wait
    pass

# Atomic literal: integer, atom, nil, char and string


def p_atomliteral_int(p):
    'atomliteral : NUMBER'
    # p[0] = AtomicLiteral(AtomicLiteralKind.INT, p[1])
    pass  # wait


def p_atomliteral_atom(p):
    'atomliteral : ATOM'
    # p[0] = AtomicLiteral(AtomicLiteralKind.ATOM, p[1])
    pass  # wait


def p_atomliteral_nil(p):
    'atomliteral : nil'
    # p[0] = AtomicLiteral(AtomicLiteralKind.NIL, p[1])
    pass  # wait


def p_atomliteral_char(p):
    'atomliteral : CHAR'
    # p[0] = AtomicLiteral(AtomicLiteralKind.CHAR, p[1])
    pass  # wait


def p_atomliteral_string(p):
    'atomliteral : STRING'
    # p[0] = AtomicLiteral(AtomicLiteralKind.STRING, p[1])
    pass  # wait


def p_nil(p):
    # Nil : []
    'nil : LBRACK RBRACK'
    # p[0] = []
    pass  # wait


# constant: atomic literal, { } , {...} , [...] and [...|.]
def p_constant_atom(p):
    'constant : atomliteral'
    # p[0] = Constant(ConstantKind.ATOM, p[1])
    pass  # wait


def p_constant_bracenone(p):
    'constant : LBRACE RBRACE'
    # p[0] = Constant(ConstantKind.BRACE, None)
    pass  # wait


def p_constant_brace(p):
    'constant : LBRACE constants RBRACE'
    # p[0] = Constant(ConstantKind.BRACE, p[2])
    pass  # wait


def p_constant_brack(p):
    'constant : LBRACK constants RBRACK'
    # p[0] = Constant(ConstantKind.BRACK, p[2])
    pass  # wait


def p_constant_brackvbar(p):
    'constant : LBRACK constants VBAR constant RBRACK'
    # p[0] = Constant(ConstantKind.BRACK, p[2].append(p[4]))
    pass  # wait


def p_constants_one(p):
    'constants : constant'
    # p[0] = []
    # p[0].append(p[1])
    pass  # wait


def p_constants_combine(p):
    'constants : constants COMMA constant'
    # p[0] = p[1]
    # p[0].append(p[3])
    pass  # wait


def p_functionname(p):
    'functionname : ATOM SLASH NUMBER'
    # p[0] = FunctionName(p[1], p[3])
    pass  # wait


def p_functionnames_one(p):
    'functionnames : functionname'
    # p[0] = []
    # p[0].append(p[1])
    pass  # wait


def p_functionnames_combine(p):
    'functionnames : functionnames COMMA functionname'
    # p[0] = p[1]
    # p[0].append(p[3])
    pass  # wait


def p_attributes(p):
    'attributes : ATTRIBUTES LBRACK moduleattributes RBRACK'
    # wait
    pass


def p_moduleattribute(p):
    'moduleattribute : ATOM EQUAL constant'
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
    'functiondefine : afunctionname EQUAL afun'
    # wait
    pass


def p_afunctionname_notannotated(p):
    'afunctionname : functionname'
    # p[0] = p[1]
    pass  # wait


def p_afunctionname_annotated(p):
    'afunctionname : LPAREN functionname ANNOTATION LBRACK constants RBRACK RPAREN'
    # p[0] = p[2]
    pass  # wait


def p_afun_notannotated(p):
    'afun : fun'
    # p[0] = p[1]
    pass  # wait


def p_afun_annotated(p):
    'afun : LPAREN fun ANNOTATION LBRACK constants RBRACK RPAREN'
    # p[0] = p[2]
    pass  # wait


def p_expression_vlist(p):
    'expression : valuelist'
    pass  # wait


def p_expression_asingleexpression(p):
    'expression : asingleexpression'
    pass  # wait


def p_asingleexpression_se(p):
    'asingleexpression : singleexpression'
    pass  # wait


def p_asingleexpression_annotation(p):
    'asingleexpression : LPAREN singleexpression ANNOTATION LBRACK constants RBRACK RPAREN'


def p_expressions_once(P):
    'expressions : expression'
    pass  # wait


def p_expressions_combine(p):
    'expressions : expressions COMMA expression'
    pass  # wait


def p_valuelist_notempty(p):
    'valuelist : LABRACK asingleexpressions RABRACK'
    pass  # wait


def p_valuelist_empty(p):
    'valuelist : LABRACK RBRACK'
    pass  # wait


def p_asingleexpressions_one(p):
    'asingleexpressions : asingleexpression'
    pass  # wait


def p_asingleexpressions_combine(p):
    'asingleexpressions : asingleexpressions COMMA asingleexpression'
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


def p_singleexpression_call(p):
    'singleexpression : call'
    pass  # wait


def p_singleexpression_sequencing(p):
    'singleexpression : seq'
    pass  # wait


def p_singleexpression_primop(p):
    'singleexpression : primop'
    pass  # wait


def p_vars_avarname(p):
    'vars : avarname'
    pass  # wait


def p_vars_varlist(p):
    'vars : LABRACK avarnames RABRACK'
    pass  # wait


def p_vars_empty(p):
    'vars : LABRACK RABRACK'
    pass  # wait


def p_tuple_notempty(p):
    'tuple : LBRACE expressions RBRACE'
    pass  # wait


def p_tuple_empty(p):
    'tuple : LBRACE RBRACE'
    pass  # wait


def p_let(p):
    'let : LET vars EQUAL expression IN expression'
    pass  # wait


def p_list_nobar(p):
    'list : LBRACK expressions RBRACK'
    pass  # wait


def p_list_withbar(p):
    'list : LBRACK expressions VBAR expression RBRACK'
    pass  # wait


def p_application_notempty(p):
    'application : APPLY expression LPAREN expressions RPAREN'
    pass  # wait


def p_application_empty(p):
    'application : APPLY expression LPAREN RPAREN'
    pass  # wait


def p_fun(p):
    'fun : FUN LPAREN avarnames RPAREN ARROW expression'
    pass  # wait


def p_fun_empty(p):
    'fun : FUN LPAREN RPAREN ARROW expression'
    pass  # wait


def p_apattern_var(p):
    'apattern : avarname'
    pass  # wait


def p_apattern_pattern(p):
    'apattern : pattern'
    pass  # wait


def p_pattern_atomicliteral(p):
    'pattern : atomliteral'
    pass  # wait


def p_pattern_brace(p):
    'pattern : LBRACE apatterns RBRACE'
    pass  # wait


def p_pattern_braceempty(p):
    'pattern : LBRACE RBRACE'
    pass  # wait


def p_pattern_brack(p):
    'pattern : LBRACK apatterns RBRACK'
    pass  # wait


def p_pattern_brackwithbar(p):
    'pattern : LBRACK apatterns VBAR apattern RBRACK'
    pass  # wait


def p_pattern_varname(p):
    'pattern : avarname EQUAL apattern'
    pass  # wait


def p_avarname_varname(p):
    'avarname : VARNAME'
    pass  # wait


def p_avername_annotation(p):
    'avarname : LPAREN VARNAME ANNOTATION LBRACK constants RBRACK RPAREN'
    pass  # wait


def p_avarnames_once(p):
    'avarnames : avarname'
    pass  # wait


def p_avarnames_combine(p):
    'avarnames : avarnames COMMA avarname'
    pass  # wait


def p_apatterns_once(p):
    'apatterns : apattern'
    pass  # wait


def p_apatterns_combine(p):
    'apatterns : apatterns COMMA apattern'
    pass  # wait


def p_patterns_pattern(p):
    'patterns : apattern'
    pass  # wait


def p_patterns_patternlist(p):
    'patterns : LABRACK apatterns RABRACK'
    pass  # wait


def p_patterns_empty(p):
    'patterns : LABRACK RABRACK'
    pass  # wait


def p_clause(p):
    'clause : patterns guard ARROW expression'
    pass  # wait


def p_guard(p):
    'guard : WHEN expression'
    pass  # wait


def p_aclause_noa(p):
    'aclause : clause'
    pass  # wait


def p_aclause_witha(p):
    'aclause : LPAREN clause ANNOTATION LBRACK constants RBRACK RPAREN'


def p_case(p):
    'case : CASE expression OF aclauses END'
    pass  # wait


def p_aclauses_once(p):
    'aclauses : aclause'
    pass  # wait


def p_aclauses_combine(p):
    'aclauses : aclauses aclause'
    pass  # wait


def p_receive(p):
    'receive : RECEIVE aclauses timeout'
    pass  # wait


def p_timeout(p):
    'timeout : AFTER expression ARROW expression'
    pass  # wait


def p_call_notempty(p):
    'call : CALL expression COLON expression LPAREN expressions RPAREN'
    pass  # wait


def p_call_empty(p):
    'call : CALL expression COLON expression LPAREN RPAREN'
    pass  # wait


def p_seq(p):
    'seq : DO expression expression'
    pass  # wait


def p_primop_notempty(p):
    'primop : PRIMOP ATOM LPAREN expressions RPAREN'
    pass  # wait


def p_primop_empty(p):
    'primop : PRIMOP ATOM LPAREN RPAREN'
    pass  # wait


parser = yacc.yacc()

# str = "examples/concdb.core"
# str = "examples/finite_leader.core"
# str = "examples/firewall.core"
# str = "examples/howait.core"
# str = "examples/parikh.core"
# str = "examples/pipe.core"
# str = "examples/race.core"
# str = "examples/reslock.core"
# str = "examples/ring.core"
# str = "examples/safe_send.core"
# str = "examples/sieve.core"
# str = "examples/state_factory.core"
# str = "examples/stutter.core"
str = "examples/unsafe_send.core"
filein = open(str)
data = filein.read()
result = parser.parse(data, lexer=lexer)
