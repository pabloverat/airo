# airo.py

import ply.lex as lex
import ply.yacc as yacc

import tokrules as tokrules
from tokrules import tokens
from grammar import *

import sys
from utils import read_file, print_tokens
from output_formatter import Output_Formatter

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
    
    # "parseando"
    _ = myParser.parse(data, lexer=myLexer)
    print("terminé el parsing\n")
    
    # directorio de funciones
    print("dir_funcs:\n")
    myParser.dir_funcs.print_funcs()
    
    # tabla de constantes
    print("const_table:\n")
    myParser.const_table.print()
    
    # pilas
    print("pOperadores: ", myParser.cuads.pilaOperadores)
    print("pOperandos: ", myParser.cuads.pilaOperandos)
    print("pTipos: ", myParser.cuads.pilaTipos)
    print("pSaltos: ", myParser.cuads.pilaSaltos)
    
    # cuádruplos
    print("\ncuádruplos con direcciones:\n")
    myParser.cuads.print()
    print("\ncuádruplos con nombres:\n")
    myParser.aux_cuads.print()
    
    
    out = Output_Formatter()
    out.cuads = myParser.cuads.get_ovejota_str()
    out.consts = myParser.const_table.get_ovejota_str()
    out.dir_funcs = myParser.dir_funcs.get_ovejota_str()
    out.build_ovejota()

    
    
if __name__ == "__main__":
    main()