# airo.py

import ply.lex as lex
import ply.yacc as yacc

import tokrules as tokrules
from tokrules import tokens
from grammar import *

from tabla_vars import Tabla_Vars

import sys
from utils import read_file, print_tokens

# entry point
def main():

# función para actuar en caso de errores en la sintaxis
    def p_error(p):
        if p:
            print('Syntax/Parsing error at token', p, "\n")
            # myParser.errok()
            myParser.restart()
        else:
            print('error: not p')
            
        exit()
                    
    # comprobando que se enviaron dos argumentos en el comando de la terminal         
    if len(sys.argv) != 2:
        print('Usage: python airo.py <filename>')
        exit()
        
    # obteniendo archivo de código a compilar
    fname = sys.argv[1]
    data = read_file(fname)

    # construyendo scanner
    myLexer = lex.lex(module=tokrules)
    myLexer.input(data)

    # imprimiendo tokens
    print_tokens(myLexer)

    # construyendo parser
    myParser = yacc.yacc()
    myParser.vars_table = Tabla_Vars()
    _ = myParser.parse(data, lexer=myLexer)
    print(myParser.test)
    print("terminé el parsing")
    
    print("vars table:")
    myParser.vars_table.print_vars()
    
        
if __name__ == "__main__":
    main()