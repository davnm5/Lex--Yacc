import re
import numpy as np

linea=0
tokens = (
    'NUMPY','ARANGE','ARGMAX','ARGMIN','SUM','WHERE',
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN','POTENCY','DIVIDE_INT','STR','LIST', 'ARRAY', 'RESHAPE', 'SUM' , 'MEAN','POINT','PRINT','IF','ELSE','MENORQUE',
    'TAB','DOSPUNTOS','MAYORQUE','DIFERENTE','DIGUAL','LINE','OR','AND','COMA','LCORCHETE','RCORCHETE'
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
t_COMA=r'\,'
t_LCORCHETE  = r'\['
t_RCORCHETE  = r'\]'


def t_DOSPUNTOS(t):
    r'\:'
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
    r'else'
    t.value = t.value
    return t
    
def t_MEAN(t) :
    r'mean'
    t.value = t.value
    return t

def t_ARANGE(t):
    r'arange'
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
    r'(\'(\s*\w*\S*)*\')|(\"(\s*\w*\S*)*\")'
    t.value =t.value
    return t

def t_DIFERENTE(t):
    r'!='
    t.value=t.value
    return t

def t_DIGUAL(t):
    r'=='
    t.value=t.value
    return t

def t_ARGMAX(t):
    r'argmax'
    t.value = t.value
    return t

def t_ARGMIN(t):
    r'argmin'
    t.value = t.value
    return t

def t_SUM(t):
    r'sum'
    t.value = t.value
    return t

def t_WHERE(t):
    r'where'
    t.value = t.value
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
                 | expression_numpy '''


    aux=str(p[1])
    print(re.sub('"', "", re.sub("'","",aux)))


def p_print(p):
    '''statement : TAB PRINT LPAREN STR COMA expression RPAREN
            | PRINT LPAREN STR COMA expression RPAREN
            | PRINT LPAREN expression RPAREN
            | TAB PRINT LPAREN expression RPAREN  '''
    

def p_print_error(p):
    ''' statement : PRINT
             | PRINT expression
             | PRINT LPAREN expression
             | PRINT LPAREN
             | PRINT TAB expression''' 
    
    print("ERROR: Sintaxis incorrecta en PRINT ")


def p_statement_assign(p):
    '''expresasign : NAME EQUALS expression
                   | NAME EQUALS expression_numpy '''
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
    ''' condition : expression DIGUAL expression
    | expression DIFERENTE expression
    | expression MAYORQUE expression
    | expression MENORQUE expression
    | condition TAB AND TAB condition
    | condition TAB OR TAB condition '''

def p_if(p):
    ''' statement : IF LPAREN condition RPAREN DOSPUNTOS
    '''

def p_if_error(p):
    ''' statement : IF LPAREN condition RPAREN
    | IF TAB condition DOSPUNTOS
    | IF LPAREN condition
    | IF LPAREN 
    | IF LPAREN expression
    | IF LPAREN condition DOSPUNTOS '''
    
    print("ERROR: Sintaxis incorrecta en la sentencia IF ")

def p_where(p):
    ''' where : LPAREN condition_where COMA NAME COMA expression RPAREN '''
    
    try:
        
        if(str(p[6]).startswith("[") and str(p[6]).endswith("]")):
            print("El tercer argumento de where no puede ser una lista")
            
        if(not str(names[p[4]]).startswith("np.array(") and not str(names[p[4]]).endswith(")")):
            print("Error: En el segundo argumento la variable %s debe contener un array" %p[4])   
    except:
        print(" posi La variable %s no esta definida" %p[4])
    

def p_condition_where(p):
    ''' condition_where : NAME MENORQUE NUMBER
                        | NAME MAYORQUE NUMBER
                        | NAME DIGUAL NUMBER ''' 
    try:
        if(not str(names[p[1]]).startswith("np.array(") and not str(names[p[1]]).endswith(")")):
            print("Error: En el primer argumento la variable %s debe contener un array"%p[1])   
    except:
        print("La variable %s no esta definida" %p[1])
                
def p_else(p):
    ''' statement : ELSE DOSPUNTOS '''

def p_else_error(p):
    ''' 
    statement : ELSE
    
    '''
    print("ERROR: Sintaxis incorrecta en la sentencia ELSE ")


def p_expresion_numpy(p):
    'expression_numpy : NUMPY POINT numpyfunc'
    if(p[3]!=None): p[0] = p[1]+ str(p[2])+p[3]


def p_numpyfuncion(p):
    '''numpyfunc : ARRAY array
                 | ARANGE arange
                 | ARANGE arange_error
                 | ARRAY array_error
                 | ARGMAX argmax
                 | ARGMAX argmax_error
                 | ARGMIN argmin
                 | ARGMIN argmin_error
                 | SUM sum
                 | SUM sum_error
                 | WHERE where '''
    p[0] = p[1]+str(p[2])
    

def p_array(p):
    ''' array : LPAREN NAME RPAREN
                 | LPAREN NUMBER RPAREN
                 | LPAREN expression RPAREN
    '''
    try:
        p[0]=str(p[1])+str(p[2])+str(p[3])
        if(not names[p[2]].startswith("[") and not names[p[2]].endswith("]")):
            print("ERROR: La variable no contiene una lista")
        else:
            p[0]=p[2]
            
        
    except:
        print("")
    
def p_array_error(p):
    '''
    array_error : LPAREN STR RPAREN
    '''    
    print("ERROR: El argumento de array debe ser una lista")

def p_arange(p):
    ''' arange : LPAREN NUMBER RPAREN
                | LPAREN NAME RPAREN '''
    
    try:
        p[0]=str(p[1])+str(p[2])+str(p[3])
        if(not str(names[p[2]]).isdigit()):
            print("ERROR: La variable no contiene un digito")
        else:
            p[0]="("+str(p[2])+")"
             
    except: 
        print("")
   
    
def p_arange_error(p):
    ''' arange_error : LPAREN STR RPAREN '''
    print("Error: El argumento de arange debe ser un numero")

def p_argmin(p):
    '''argmin : LPAREN NAME RPAREN
                | LPAREN expression RPAREN '''
    try:
        p[0]=str(p[1])+str(p[2])+str(p[3])
        if(not names[p[2]].startswith("[") and not names[p[2]].endswith("]")):
            print("ERROR: La variable no contiene un array")
        else:
            p[0]=p[2]
    except:
        print("")

def p_argmax(p):
    ''' argmax : LPAREN NAME RPAREN
                | LPAREN expression RPAREN '''
    try:
        p[0]=str(p[1])+str(p[2])+str(p[3])
        if(not names[p[2]].startswith("[") and not names[p[2]].endswith("]")):
            print("ERROR: La variable no contiene un array")
        else:
            p[0]=p[2]
    except:
        print("")
        
def p_argmin_error(p):
    '''
    argmin_error : LPAREN STR RPAREN
    '''    
    print("ERROR: El argumento de argmin debe ser un array")

def p_argmax_error(p):
    '''
    argmax_error : LPAREN STR RPAREN
    '''    
    print("ERROR: El argumento de argmax debe ser un array")
    
def p_sum(p):
    ''' sum : LPAREN NAME RPAREN
                | LPAREN expression RPAREN '''
    try:
        p[0]=str(p[1])+str(p[2])+str(p[3])
        if(not names[p[2]].startswith("[") and not names[p[2]].endswith("]")):
            print("ERROR: La variable no contiene una lista")
        else:
            p[0]=p[2]
    except:
        print("")

def p_sum_error(p):
    '''
    sum_error : LPAREN STR RPAREN
    '''    
    print("ERROR: El argumento de sum debe ser una lista")   
    
def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] =int(p[1])

def p_expresion_str(p):
    'expression : STR'
    p[0]= str(p[1])

def p_expression_lst(p):
    ''' expression : LCORCHETE expression_list RCORCHETE 
                    | LCORCHETE RCORCHETE
                    | list_error '''
    try:
        p[0]=str(p[1])+str(p[2])+str(p[3])
    except:
        print("")

def p_expression_lst_error(p):
    ''' list_error : LCORCHETE expression_list
                   | LCORCHETE expression_list COMA '''
    print("Error: Falta el caracter ']' en la lista ")


def p_expresion_list(p):
    ''' expression_list :  expression COMA expression_list
                        | expression '''
    
    try:
        p[0]=str(p[1])+str(p[2])+str(p[3])
    except:
        p[0]=str(p[1])
    
   
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

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

        except EOFError:
            print("error lexer")
