# grammar.py

from utils import print_control, encode_var_type, encode_func_type


#--- START : funciones de la gramática formal ---

def p_start(p):
    '''program : encabezamiento var_list func_list cuerpo
               | encabezamiento var_list cuerpo
               | encabezamiento func_list cuerpo
               | encabezamiento cuerpo
    '''
    print_control(p, "S\t", 4)
    p.parser.test = "test"

def p_encabezamiento(p):
    '''encabezamiento : PROGRAM ID context_to_global
    '''
    print_control(p, "encabezamiento", 2)
    
def p_context_to_global(p):
    "context_to_global : "
    p.parser.context = 0 # 0 for globals, 1 for locals
    print("Parsed context_to_global\t", p.parser.context)

def p_cuerpo(p):
    '''cuerpo : MAIN context_to_global OPPARENTH CLPARENTH OPBRACE estat_list CLBRACE
    '''
    print_control(p, "cuerpo\t", 6)

def p_variable(p):
    '''variable : VAR ID COLON var_typ
                | VAR ID COLON var_typ dims
    '''
    print_control(p, "var\t", 5)
    p.parser.vars_table.add_var(p.parser.context, p[2], p.parser.var_type_read)

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
    print_control(p, "param_list", 2)
    
def p_dims(p):
    '''dims : OPBRACKET aritm CLBRACKET
            | OPBRACKET aritm CLBRACKET OPBRACKET CONST_INT CLBRACKET
    '''
    print_control(p, "dims\t", 6)

def p_func(p):
    '''func : FUNC context_to_local ID OPPARENTH CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE
            | FUNC context_to_local ID OPPARENTH param_list CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE
    '''
    print_control(p, "func\t", 10)

def p_context_to_local(p):
    "context_to_local :"
    #print_control(p, "context_to_local", 0)
    p.parser.context = 1 # 0 for globals, 1 for locals
    print("Parsed context_to_local\t", p.parser.context)

def p_ciclo(p):
    '''ciclo : WHILE OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE
    '''
    print_control(p, "ciclo\t", 8)

def p_decision(p):
    '''decision : WHEN OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE
               | WHEN OPPARENTH logic CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE OPBRACE estat_list CLBRACE
    '''
    print_control(p, "decision", 12)

def p_func_cont(p):
    '''func_cont : var_list estat_list RETURN expr
                 | estat_list RETURN expr
                 | var_list estat_list
                 | estat_list
    '''
    print_control(p, "func_cont", 5)

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
    p.parser.vars_table.add_var(p.parser.context, p[1], p.parser.var_type_read)

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
    '''
    print_control(p, "factor\t", 3)

def p_logic(p):
    '''logic : oprnd AND logic
             | oprnd OR logic
             | NOT oprnd
             | oprnd
    '''
    print_control(p, "logic\t", 3)

def p_expr(p):
    '''expr : aritm
            | logic
            | ID OPPARENTH CLPARENTH
            | ID OPPARENTH args CLPARENTH
    '''
    print_control(p, "expr\t", 1)

def p_oprnd(p):
    '''oprnd : FALSE
             | TRUE
             | relac
             | OPPARENTH logic CLPARENTH
    '''
    print_control(p, "oprnd\t", 3)

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
    '''args : expr COMMA args
            | expr
    '''
    print_control(p, "args\t", 4)
    
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
    print_control(p, "llam_void", 3)

def p_asign(p):
    '''asign : ID ASGNMNT lectura
             | ID ASGNMNT expr
             | ID ASGNMNT CONST_STRING
             | ID dims ASGNMNT lectura
             | ID dims ASGNMNT expr
             | ID dims ASGNMNT CONST_STRING
    '''
    print_control(p, "asign\t", 7)

#--- END : funciones de la gramática formal ---