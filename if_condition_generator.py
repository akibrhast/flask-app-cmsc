import ply.lex as lex

 # List of token names.   This is always required
 

# data = '''
# if ( X0 == 11 ) {
# X10 = X0 ;
# }
# else {
# X10 = -11 ;
# }'''
# data1 = '''if ( X12 > 9 ) {X3 = X12}else {X3 = X12}'''



reserved = {'if' : 'IF',
'then' : 'THEN',
'else' : 'ELSE',
'while' : 'WHILE',}

tokens = ['NUMBER',
'PLUS',
'MINUS',
'TIMES',
'DIVIDE',
'LPAREN',
'RPAREN',
'VARIABLE',
'LCURLY',
'RCURLY',
'LESSTHAN',
'GREATERTHAN',
'LESSTHANEQUAL',
'GREATERTHANEQUAL',
'NOTEQUAL',
'EQUALEQUAL',
'EQUALTO'
]+ list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCURLY  = r'\{'
t_RCURLY  = r'\}'
t_LESSTHAN = r'\<'
t_LESSTHANEQUAL = r'\<='
t_GREATERTHANEQUAL = r'\>='
t_GREATERTHAN = r'\>'
t_EQUALTO = r'\='
t_EQUALEQUAL = r'\=='
t_NOTEQUAL = r'\!='

 
def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')    # Check for reserved words
    
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n+;'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex()


import ply.yacc as yacc



# Error rule for syntax errors
def p_error(p):
    print(p)



def p_ifCond(p):
    'expression : IF condition expression ELSE expression'
    p[0] = "IF:   " + p[2] + "\n" + "THEN: " + p[3] + "\n" +"      B ENDIF"+"\n" + "ELSE: " + p[5] + "\n" + "ENDIF:"


def p_cond(p):
    '''condition : LPAREN sign_variable GREATERTHAN sign_variable RPAREN
                 | LPAREN sign_variable GREATERTHANEQUAL sign_variable RPAREN
                 | LPAREN sign_variable LESSTHAN sign_variable RPAREN
                 | LPAREN sign_variable LESSTHANEQUAL sign_variable RPAREN
                 | LPAREN sign_variable NOTEQUAL sign_variable RPAREN
                 | LPAREN sign_variable EQUALEQUAL sign_variable RPAREN'''
    
    conditional_dict = { ">"  : "B.LE ELSE",
                         ">=" : "B.LT ELSE",
                         "<"  : "B.GE ELSE",
                         "<=" : "B.GT ELSE",
                         "==" : "B.NE ELSE",
                         "!=" : "B.EQ ELSE"} 

    
    if(('-' in p[4]) and (p[4].replace("-","").isdigit())):
        p[0] = "ADDIS " + "XZR,"+p[2].replace("-","") +","+ "#" +p[4].replace("-","") + "\n      " + conditional_dict[p[3]]
    elif '-' in p[4]:
        p[0] = "ADDS " + "XZR,"+p[2].replace("-","") +","+p[4].replace("-","") + "\n      " + conditional_dict[p[3]]
    elif p[4].replace("-","").isdigit():
        p[0] = "SUBSIS " + " XZR," + p[2].replace("-","") + "," + p[4].replace("-","")+ "\n      " + conditional_dict[p[3]]
    else:
        p[0] = "SUBS " + " XZR," + p[2].replace("-","") + "," + p[4].replace("-","")+ "\n      " + conditional_dict[p[3]]

def p_expression(p):
    'expression : LCURLY sign_variable EQUALTO sign_variable RCURLY'

    if(('-' in p[4]) and (p[4].replace("-","").isdigit()) ):
        p[0] = "ADDI " + p[2] + "," + "XZR," + "#" +p[4]
    elif( ('-' not in p[4]) and (p[4].replace("-","").isdigit())):
        p[0] = "ADDI " + p[2] + "," + "XZR," + "#" +p[4]
    elif( [not (p[4].replace("-","").isdigit())]  and [ ('-' in p[4]) ]  ):
        p[0] = "ADD " + p[2] + "," + p[4] + ",XZR"
    
    #p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_sign_variable(p):
    '''sign_variable : sign VARIABLE
                     | sign NUMBER'''
    if p[1] == None:
        p[0] = str(p[2])
    else:
        p[0] = str(p[1]) + str(p[2])



def p_sign(p):
    '''sign : empty
            | MINUS'''
    p[0] = p[1]


    
def p_empty(p):
    'empty :'
    pass
# Build the parser
parser = yacc.yacc()
# result = parser.parse(data)
# print(result)
'''
a>b  : a-b>0  ; cond = b.le
a>-b : a+b>0  ; cond = b.le
a==b : a-b=0
a<b  : a-b<0  ; cond = b.ge
a>=b : a-b>=0 ; cond = b.lt
a<=b : a-b<=0 ; cond = b.le
a!=b : a-b    ; cond = b.eq
a==b : a-b    ; cond = b.ne
'''


# Give the lexer some input
#lexer.input(data)



# for tok in lexer:
#     print(tok)
