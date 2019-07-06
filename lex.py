import re
import numpy as np


linea=0
tokens = (
    'NUMPY',
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN','POTENCY','DIVIDE_INT','STR','LIST', 'ARRAY', 'RESHAPE', 'SUM' , 'MEAN','POINT','PRINT','IF','ELSE','MENORQUE',
    'TAB','DOSPUNTOS','MAYORQUE','DIFERENTE','DIGUAL','LINE','OR','AND'
    )

# Tokens
t_POINT = r'\.'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_POTENCY = r'\*{2}'
t_DIVIDE_INT = r'\/{2}'
t_MENORQUE = r'\<'
t_MAYORQUE= r'\>'
t_TAB= r'[ \t]'


def t_DOSPUNTOS(t):
    r':'
    t.value = t.value
    return t

def t_NUMPY(t):
    r'np'
    t.value = t.value
    return t

def t_AND(t):
    r'and'
    t.value = t.value
    return t

def t_OR(t):
    r'or'
    t.value = t.value
    return t

def t_PRINT(t):
    r'print'
    t.value = t.value
    return t

def t_IF(t):
    r'if'
    t.value = t.value
    return t

def t_ELSE(t):
    r'else:'
    t.value = t.value
    return t
    
def t_MEAN(t) :
    r'mean'
    t.value = t.value
    return t

def t_SUM(t) :
    r'sum'
    t.value = t.value
    return t

def t_RESHAPE(t) :
    r'reshape'
    t.value = t.value
    return t

def t_ARRAY (t):
    r'array'
    t.value = t.value
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STR(t):
    r'(\'(\s*\w*\S*)+\')|(\"(\s*\w*\S*)+\")'
    t.value =t.value
    return t

def t_LIST(t):
    r'(\[((\d+|\"\S*\W*\S*\")(\,(\d+|\"\S*\W*\S*\"))*)*\])'
    t.value=t.value
    return t

def t_DIFERENTE(t):
    r'!='
    t.value=t.value
    return t

def t_DIGUAL(t):
    r'=='
    t.value=t.value
    return t
    
    

def t_error(t):
    print("Caracter no válido '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lex.lex()


precedence = (
    ('right' , 'EQUALS'),
    ('right' , 'NAME'),
    ('right','NUMPY','POINT'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

names = { }




def p_statement_expr(p):
    '''statement : expression
                 | expresasign
                 | if
                 | print
                 | else '''


    aux=str(p[1])
    print(re.sub('"', "", re.sub("'","",aux)))


def p_print(p):
    '''print : TAB PRINT LPAREN expression RPAREN
            | PRINT LPAREN expression RPAREN
            | ELSE print'''


def p_statement_assign(p):
    '''expresasign : NAME EQUALS expression
                   | NAME EQUALS exprenumpy'''
    names[p[1]] = p[3]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POTENCY expression
                  | expression DIVIDE_INT expression'''
    try:
        if p[2] == '+': p[0] = p[1] + p[3]
        elif p[2] == '-': p[0] = p[1] - p[3]
        elif p[2] == '*': p[0] = p[1] * p[3]
        elif p[2] == '/': p[0] = p[1] / p[3]
        elif p[2]== '**':  p[0]= p[1] ** p[3]
        elif p[2]== '//':  p[0]= p[1] // p[3]

        print(p[0])
    except:
        print("La operacion no es válida")


def p_condition(p):
    ''' condition    : expression DIGUAL expression
    | expression DIFERENTE expression
    | expression MAYORQUE expression
    | expression MENORQUE expression
    | condition TAB AND TAB condition
    | condition TAB OR TAB condition '''

def p_if(p):
    ''' if    : IF LPAREN expression MENORQUE expression RPAREN DOSPUNTOS
    | IF LPAREN expression DIFERENTE expression RPAREN DOSPUNTOS
    | IF LPAREN expression DIGUAL expression RPAREN DOSPUNTOS
    | IF LPAREN expression MAYORQUE expression RPAREN DOSPUNTOS
    | IF LPAREN condition RPAREN DOSPUNTOS
    '''
    
def p_else(p):
    ''' else : ELSE
    | ELSE TAB '''

def p_expresion_numpy(p):
    'exprenumpy : NUMPY POINT numpyfunc'
    p[0] = p[1]+ str(p[2])+p[3]


def p_numpyfuncion(p):
    '''numpyfunc : ARRAY numpyarg
                 | SUM numpyarg
                 | RESHAPE numpyarg
                 | MEAN numpyarg'''

    p[0] = p[1]+p[2]


def p_numpyarg(p):
    '''numpyarg : LPAREN NAME RPAREN'''

    p[0]= "(" + p[2] +")"
    print(p[0])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expresion_str(p):
    'expression : STR'
    p[0]= str(p[1])

def p_expresion_list(p):
    'expression : LIST'
    p[0]=p[1]


def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
        print(names)
    except LookupError:
        print("La variable '%s' no esta definida " % p[1])

def p_error(p):
    if(p!=None): print("Error de sintaxis '%s'" % p)

import ply.yacc as yacc
parser=yacc.yacc()

def validar (data):
        try:
            list_temp=[]
            lex.input(data)
            while True:
                tok = lex.token()
                if not tok:
                    break
                list_temp.append(tok.type)
            print(list_temp)   
                
            result=parser.parse(data)
            if(result!=None):
                print(result)
            
        except EOFError:
            print("error lexer")
