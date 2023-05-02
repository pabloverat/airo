# airo.py

import tokrules as tokrules
import ply.lex as lex
import ply.yacc as yacc

import sys
from utils import read_file
from tokrules import tokens

def p_start(p):
    '''program : encabezamiento var_list func_list cuerpo
               | encabezamiento var_list cuerpo
               | encabezamiento func_list cuerpo
               | encabezamiento cuerpo
    '''

def p_encabezamiento(p):
    '''encabezamiento : PROGRAM ID
    '''

def p_cuerpo(p):
    '''cuerpo : MAIN OPPARENTH CLPARENTH OPBRACE estat_list CLBRACE
    '''

def p_variable(p):
    '''variable : VAR ID COLON var_typ
                | VAR ID COLON var_typ dims
    '''

def p_var_list(p):
    '''var_list : variable var_list
                | variable
    '''

def p_func_list(p):
    '''func_list : func func_list
                 | func
    '''
    
def p_estat_list(p):
    '''estat_list : estat estat_list
                  | estat
    '''

def p_param_list(p):
    '''param_list : param param_list
                  | param
    '''
    
def p_dims(p):
    '''dims : OPBRACKET CONST_INT CLBRACKET
            | OPBRACKET CONST_INT CLBRACKET OPBRACKET CONST_INT CLBRACKET
    '''

def p_func(p):
    '''func : FUNC ID OPPARENTH CLPARENTH func_typ OPBRACE func_cont CLBRACE
            | FUNC ID OPPARENTH param_list CLPARENTH func_typ OPBRACE func_cont CLBRACE
    '''

def p_ciclo(p):
    '''ciclo : WHILE OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE
    '''

def p_decision(p):
    '''decision : WHEN OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE
               | WHEN OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE OPBRACE estat_list CLBRACE
    '''

def p_func_cont(p):
    '''func_cont : var_list estat_list RETURN ID dims
                 | var_list estat_list RETURN ID
                 | estat_list RETURN ID dims
                 | var_list RETURN ID dims
                 | estat_list RETURN ID
                 | var_list RETURN ID
                 | RETURN ID dims
                 | RETURN ID
    '''

def p_estat(p):
    '''estat : asign
             | llam_void
             | lectura
             | escritura
             | carga_dt
             | decision
             | ciclo
    '''

def p_carga_dt(p):
    '''carga_dt : ID ASGNMNT LOAD OPPARENTH ID CLPARENTH
                | ID ASGNMNT LOAD OPPARENTH CONST_STRING CLPARENTH 
    '''

def p_param(p):
    '''param : ID COLON var_typ
             | ID COLON var_typ dims
    '''

def p_var_typ(p):
    '''var_typ : INT
               | FLOAT
               | CHAR
               | BOOL
               | FRAME
    '''

def p_func_typ(p):
    '''func_typ : INT
                | FLOAT
                | CHAR
                | BOOL
                | FRAME
                | VOID
    '''

def p_aritm(p):
    '''aritm : term PLUS aritm
             | term MINUS aritm
             | term
    '''

def p_term(p):
    '''term : factor TIMES term
            | factor DIVIDE term
            | factor
    '''
    
def p_factor(p):
    '''factor : OPPARENTH aritm CLPARENTH
              | ID
              | ID dims
              | CONST_INT
              | CONST_FLOAT
    '''

def p_logic(p):
    '''logic : oprnd AND logic
             | oprnd OR logic
             | NOT oprnd
             | oprnd
    '''

def p_expr(p):
    '''expr : aritm
            | logic
    '''

def p_oprnd(p):
    '''oprnd : FALSE
             | TRUE
             | relac
             | OPPARENTH logic CLPARENTH
    '''

def p_relac(p):
    '''relac : aritm EQUAL aritm
             | aritm UNEQUAL aritm
             | aritm LESS aritm
             | aritm LESSEQ aritm
             | aritm GREATER aritm
             | aritm GREATEREQ aritm
    '''

def p_args(p):
    '''args : ID dims COMMA args
            | ID COMMA args
            | ID dims
            | ID
    '''
    
def p_lectura(p):
    '''lectura : READ OPPARENTH CLPARENTH
    '''
    
def p_escritura(p):
    '''escritura : WRITE OPPARENTH ID CLPARENTH
                 | WRITE OPPARENTH ID dims CLPARENTH
                 | WRITE OPPARENTH CONST_STRING CLPARENTH
    '''

def p_llam_void(p):
    '''llam_void : OPPARENTH CLPARENTH
                 | OPPARENTH args CLPARENTH
    '''

def p_asign(p):
    '''asign : ID ASGNMNT expr
             | ID ASGNMNT CONST_STRING
             | ID ASGNMNT ID OPPARENTH CLPARENTH
             | ID ASGNMNT ID OPPARENTH args CLPARENTH
             | ID ASGNMNT lectura
             | ID dims ASGNMNT expr
             | ID dims ASGNMNT CONST_STRING
             | ID dims ASGNMNT ID OPPARENTH CLPARENTH
             | ID dims ASGNMNT ID OPPARENTH args CLPARENTH
             | ID dims ASGNMNT lectura
    '''


def p_error(p):
    if p:
        print('Syntax/Parsing error at token', p)
        # myParser.errok()
        myParser.restart()
    else:
        print('error: not p')
                
        
# def main():
    
if len(sys.argv) == 2:
    fname = sys.argv[1]
    data = read_file(fname)
    
    myLexer = lex.lex(module=tokrules)
    
    myLexer.input(data)
    
    print("tokens are:")
    # Tokenize
    while True:
        tok = myLexer.token()
        if not tok: 
            break      # No more input
        print(tok)
    
    print("terminé el scanning\n")

    myParser = yacc.yacc()
    result = myParser.parse(data)
    print("terminé el parsing")
    # print("apropiado" if result is None else "No apropiado")

else:
    print('Usage: python airo.py <filename>')
        
# if __name__ == "__main__":
#     main()