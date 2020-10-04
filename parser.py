import ply.lex as lex
import ply.yacc as yacc

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
    'of':'OF',
    'primop':'PRIMOP',
    'receive':'RECEIVE',
    'try':'TRY',
    'when':'WHEN'
}

tokens = [
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
    'ANNOTATION'
] + list(reserved.values())
