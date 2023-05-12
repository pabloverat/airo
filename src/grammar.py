# grammar.py

from utils import print_control, encode_var_type, encode_func_type
from tabla_vars import Tabla_Vars


#--- START : funciones de la gramática formal ---

def p_start(p):
    '''program : encabezamiento var_list calcula_globales func_list cuerpo
               | encabezamiento var_list calcula_globales cuerpo
               | encabezamiento func_list cuerpo
               | encabezamiento cuerpo
    '''
    print_control(p, "S\t", 5)
    

def p_calcula_globales(p):
    '''calcula_globales :
    '''
    current_func = p.parser.context
    recursos = p.parser.dir_funcs.funcs[current_func]['vars'].calculate_resources()
    p.parser.dir_funcs.funcs[current_func]['recursos'] = recursos
    print("Parsed calcula_globales")


def p_encabezamiento(p):
    '''encabezamiento : PROGRAM ID
    '''
    print_control(p, "encabezamiento", 2)
    p.parser.context = p[2] # name of active func
    func_type = encode_func_type("programa")
    globalVars = Tabla_Vars()
    p.parser.dir_funcs.add_func(func_name=p.parser.context, func_type=func_type, dir_inicio=1, vars=globalVars)


def p_context_to_global(p):
    "context_to_global : "
    # p.parser.context = 0 # 0 for globals, 1 for locals
    print("Parsed context_to_global\t")


def p_cuerpo(p):
    '''cuerpo : MAIN context_to_global OPPARENTH CLPARENTH OPBRACE estat_list CLBRACE
    '''
    print_control(p, "cuerpo\t", 7)


def p_variable(p):
    '''variable : VAR ID COLON var_typ
                | VAR ID COLON var_typ dims
    '''
    print_control(p, "var\t", 5)
    current_func = p.parser.context
    current_var_type = p.parser.var_type_read
    p.parser.dir_funcs.funcs[current_func]['vars'].add_var(p[2], current_var_type)

def p_var_list(p):
    '''var_list : variable var_list
                | variable
    '''
    print_control(p, "var_list", 2)


def p_func_list(p):
    '''func_list : func func_list
                 | func
    '''
    print_control(p, "func_list", 2)


def p_estat_list(p):
    '''estat_list : estat estat_list
                  | estat
    '''
    print_control(p, "estat_list", 2)


def p_param_list(p):
    '''param_list : param COMMA param_list 
                  | param
    '''
    print_control(p, "param_list", 3)


def p_dims(p):
    '''dims : OPBRACKET aritm CLBRACKET
            | OPBRACKET aritm CLBRACKET OPBRACKET CONST_INT CLBRACKET
    '''
    print_control(p, "dims\t", 6)


def p_func(p):
    '''func : FUNC context_to_local ID OPPARENTH CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE
            | FUNC context_to_local ID OPPARENTH param_list CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE
    '''
    print_control(p, "func\t", 11)
    func_name = p[3]
    p.parser.dir_funcs.funcs[func_name] = p.parser.dir_funcs.funcs["temp"]
    del p.parser.dir_funcs.funcs["temp"]
    p.parser.dir_funcs.funcs[func_name]['func_type'] = p.parser.func_type_read
    
    recursos = p.parser.dir_funcs.funcs[func_name]['vars'].calculate_resources()
    p.parser.dir_funcs.funcs[func_name]['recursos'] = recursos


def p_context_to_local(p):
    "context_to_local :"
    
    funcVars = Tabla_Vars()
    p.parser.context = "temp" 
    p.parser.dir_funcs.add_func(func_name=p.parser.context, func_type=None, dir_inicio=1, vars=funcVars)
    print("Parsed context_to_local\t")


def p_ciclo(p):
    # '''ciclo : WHILE OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE
    '''ciclo : WHILE OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE
    '''
    print_control(p, "ciclo\t", 8)


def p_decision(p):
    # '''decision : WHEN OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE
            #    | WHEN OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE OPBRACE estat_list CLBRACE
    '''decision : WHEN OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE
               | WHEN OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE OPBRACE estat_list CLBRACE
    '''
    print_control(p, "decision", 12)


def p_func_cont(p):
    '''func_cont : var_list estat_list RETURN aritm
                 | estat_list RETURN aritm
                 | var_list estat_list
                 | estat_list
    '''
    print_control(p, "func_cont", 4)


def p_estat(p):
    '''estat : asign
             | llam_void
             | lectura
             | escritura
             | carga_dt
             | decision
             | ciclo
    '''
    print_control(p, "estat\t", 1)


def p_carga_dt(p):
    '''carga_dt : ID ASGNMNT LOAD OPPARENTH ID CLPARENTH
                | ID ASGNMNT LOAD OPPARENTH CONST_STRING CLPARENTH 
    '''
    print_control(p, "carga_dt", 6)


def p_param(p):
    '''param : ID COLON var_typ
             | ID COLON var_typ dims
    '''
    print_control(p, "param\t", 4)
    current_func = p.parser.context
    current_var_type = p.parser.var_type_read
    p.parser.dir_funcs.funcs[current_func]['vars'].add_var(p[1], current_var_type)
    p.parser.dir_funcs.funcs[current_func]['params'] = p.parser.dir_funcs.funcs[current_func]['params']+[current_var_type]    


def p_var_typ(p):
    '''var_typ : INT
               | FLOAT
               | CHAR
               | BOOL
               | FRAME
    '''
    print_control(p, "var_typ", 1)
    p.parser.var_type_read = encode_var_type(p[1])


def p_func_typ(p):
    '''func_typ : INT
                | FLOAT
                | CHAR
                | BOOL
                | FRAME
                | VOID
    '''
    print_control(p, "func_typ", 1)
    p.parser.func_type_read = encode_func_type(p[1])


def p_aritm(p):
    '''aritm : term PLUS aritm
             | term MINUS aritm
             | term
    '''
    print_control(p, "aritm\t", 3)


def p_term(p):
    '''term : factor TIMES term
            | factor DIVIDE term
            | factor
    '''
    print_control(p, "term\t", 3)


def p_factor(p):
    '''factor : OPPARENTH aritm CLPARENTH
              | ID
              | ID dims
              | CONST_INT
              | CONST_FLOAT
              | ID OPPARENTH CLPARENTH
              | ID OPPARENTH args CLPARENTH
    '''
    print_control(p, "factor\t", 4)


# def p_logic(p):
#     '''logic : oprnd AND logic
#              | oprnd OR logic
#              | NOT oprnd
#              | oprnd
#     '''
#     print_control(p, "logic\t", 3)


# def p_expr(p):
#     '''expr : aritm
#             | logic
#             | ID OPPARENTH CLPARENTH
#             | ID OPPARENTH args CLPARENTH
#     '''
#     print_control(p, "expr\t", 1)


# def p_oprnd(p):
#     '''oprnd : FALSE
#              | TRUE
#              | relac
#              | OPPARENTH logic CLPARENTH
#     '''
#     print_control(p, "oprnd\t", 3)


def p_relac(p):
    '''relac : aritm EQUAL aritm
             | aritm UNEQUAL aritm
             | aritm LESS aritm
             | aritm LESSEQ aritm
             | aritm GREATER aritm
             | aritm GREATEREQ aritm
    '''
    print_control(p, "relac\t", 3)


def p_args(p):
    '''args : aritm COMMA args
            | aritm
    '''
    print_control(p, "args\t", 3)


def p_lectura(p):
    '''lectura : READ OPPARENTH CLPARENTH
    '''
    print_control(p, "lectura", 3)


def p_escritura(p):
    '''escritura : WRITE OPPARENTH ID CLPARENTH
                 | WRITE OPPARENTH ID dims CLPARENTH
                 | WRITE OPPARENTH CONST_STRING CLPARENTH
    '''
    print_control(p, "escritura", 5)


def p_llam_void(p):
    '''llam_void : ID OPPARENTH CLPARENTH
                 | ID OPPARENTH args CLPARENTH
    '''
    print_control(p, "llam_void", 4)


def p_asign(p):
    '''asign : ID ASGNMNT lectura
             | ID ASGNMNT aritm
             | ID ASGNMNT CONST_STRING
             | ID dims ASGNMNT lectura
             | ID dims ASGNMNT aritm
             | ID dims ASGNMNT CONST_STRING
    '''
    print_control(p, "asign\t", 4)

#--- END : funciones de la gramática formal ---