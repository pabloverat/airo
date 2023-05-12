# airo.py

import ply.lex as lex
import ply.yacc as yacc

import tokrules as tokrules
from tokrules import tokens
from grammar import *

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
    
    # agregando directorio de funciones
    # myParser.dir_funcs = Dir_Funcs()
    
    # "parseando"
    _ = myParser.parse(data, lexer=myLexer)
    print("terminé el parsing\n")
    
    # directorio de funciones
    print("dir_funcs:\n")
    myParser.dir_funcs.print_funcs()
    
    # cuádruplos
    print("cuádruplos:\n")
    myParser.cuads.print()
    
        
if __name__ == "__main__":
    main()