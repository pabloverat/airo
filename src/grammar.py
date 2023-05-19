# grammar.py

from utils import print_control, encode_var_type, encode_func_type
from dir_funcs import Dir_Funcs
from tabla_vars import Tabla_Vars
from cuadruplos import Cuadruplos
from cubo import ENCODE, CUBO

#--- START : funciones de la gramática formal ---

def p_start(p):
    '''program : encabezamiento var_list func_list cuerpo
               | encabezamiento var_list cuerpo
               | encabezamiento func_list cuerpo
               | encabezamiento cuerpo
    '''
    print_control(p, "S\t", 5)
    # DELETE DIR_FUNC AND GLOBAL VAR_TABLE
    

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
    p.parser.dir_funcs = Dir_Funcs() # create dirFunc
    p.parser.cuads = Cuadruplos() # create cuadruplos list
    p.parser.cuads.add_cuadruplo(operation=ENCODE['GOTO'])
    
    p.parser.context = p[2] # name of active func
    p.parser.programName= p.parser.context
    func_type = encode_func_type("programa") # type of active func
    globalVars = Tabla_Vars()
    p.parser.dir_funcs.add_func(func_name=p.parser.context, func_type=func_type, dir_inicio=1, vars=globalVars)
    
    print_control(p, "encabezamiento", 2)


def p_context_to_global(p):
    "context_to_global : "
    p.parser.context = p.parser.programName
    current_cuad = len(p.parser.cuads.cuadruplos)
    p.parser.cuads.cuadruplos[0].result = current_cuad
    print("Parsed context_to_global\t")


def p_cuerpo(p):
    '''cuerpo : MAIN context_to_global OPPARENTH CLPARENTH OPBRACE estat_list calcula_globales CLBRACE
    '''
    print_control(p, "cuerpo\t", 8)


def p_variable(p):
    '''variable : VAR ID COLON var_typ
                | VAR ID COLON var_typ dims
    '''
    p[0] = p[2]
    current_func = p.parser.context
    p.parser.dir_funcs.funcs[current_func]['vars'].add_var(p[2], ENCODE[p[4]])
    print_control(p, "var\t", 5)


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


def p_save_array_size(p):
    '''save_array_size : 
    '''
    p[0] = p.parser.cuads.pilaOperandos.pop()
    p.parser.cuads.pilaTipos.pop()
    # print("save_array_size")


def p_dims(p):
    '''dims : OPBRACKET aritm save_array_size CLBRACKET
            | OPBRACKET aritm save_array_size CLBRACKET OPBRACKET aritm save_array_size CLBRACKET
    '''
    print_control(p, "dims\t", 6)
    


def p_func(p):
    '''func : FUNC context_to_local ID OPPARENTH CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE
            | FUNC context_to_local ID OPPARENTH param_list CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE
    '''
    func_name = p[3]
    p[0] = func_name
    
    # check if the function's name is already used
    if func_name in p.parser.dir_funcs.funcs.keys():
        raise Exception(f"func {func_name} already exists")
    
    # agregar nombre y tipo de función a temporal que estaba en dirfunc
    p.parser.dir_funcs.funcs[func_name] = p.parser.dir_funcs.funcs["temp"]
    del p.parser.dir_funcs.funcs["temp"]
    p.parser.dir_funcs.funcs[func_name]['func_type'] = p.parser.func_type_read
    
    # agregar recursos utilizados por función
    recursos = p.parser.dir_funcs.funcs[func_name]['vars'].calculate_resources()
    p.parser.dir_funcs.funcs[func_name]['recursos'] = recursos
    
    print_control(p, "func\t", 11)


def p_context_to_local(p):
    "context_to_local :"
    
    funcVars = Tabla_Vars()
    p.parser.context = "temp" 
    dir_inicio = len(p.parser.cuads.cuadruplos)
    p.parser.dir_funcs.add_func(func_name=p.parser.context, func_type=None, dir_inicio=dir_inicio, vars=funcVars)
    print("Parsed context_to_local\t")


def p_ciclo_q1(p):
    '''ciclo_q1 : 
    '''
    p.parser.cuads.pilaSaltos.append(len(p.parser.cuads.cuadruplos))

    
def p_ciclo_q2(p):
    '''ciclo_q2 :
    '''
    end = p.parser.cuads.pilaSaltos.pop()
    ret = p.parser.cuads.pilaSaltos.pop()
    p.parser.cuads.add_cuadruplo(operation=ENCODE["GOTO"], result=ret)
    p.parser.cuads.cuadruplos[end-1].result = len(p.parser.cuads.cuadruplos)
        

def p_ciclo(p):
    '''ciclo : WHILE ciclo_q1 OPPARENTH relac conditional_q1 CLPARENTH THEN OPBRACE estat_list CLBRACE ciclo_q2
    '''
    print_control(p, "ciclo\t", 8)


def p_conditional_q1(p):
    '''conditional_q1 : 
    '''
    p.parser.cuads.add_cuadruplo(operation=ENCODE["GOTOF"], leftOp=p[-1])
    p.parser.cuads.pilaSaltos.append(len(p.parser.cuads.cuadruplos))
    # print("conditional_q1", p[-1])


def p_conditional_q2(p):
    '''conditional_q2 : 
    '''
    else_cuad = len(p.parser.cuads.cuadruplos)
    gotof_cuad = p.parser.cuads.pilaSaltos.pop()
    p.parser.cuads.cuadruplos[gotof_cuad-1].result = else_cuad

    
def p_conditional_q3(p):
    '''conditional_q3 : 
    '''
    p.parser.cuads.add_cuadruplo(operation=ENCODE["GOTO"])
    false = p.parser.cuads.pilaSaltos.pop()
    p.parser.cuads.pilaSaltos.append(len(p.parser.cuads.cuadruplos))
    
    p.parser.cuads.cuadruplos[false-1].result = len(p.parser.cuads.cuadruplos)
    

def p_decision(p):
    '''decision : WHEN OPPARENTH relac conditional_q1 CLPARENTH THEN OPBRACE estat_list CLBRACE conditional_q2
                | WHEN OPPARENTH relac conditional_q1 CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE conditional_q3 OPBRACE estat_list CLBRACE conditional_q2
    '''
    print_control(p, "decision", 16 )


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
    p[0] = p[1]
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
    p[0] = p[1]
    current_func = p.parser.context
    p.parser.dir_funcs.funcs[current_func]['vars'].add_var(p[1], ENCODE[p[3]])
    p.parser.dir_funcs.funcs[current_func]['params'] = p.parser.dir_funcs.funcs[current_func]['params']+[ENCODE[p[3]]]    
    print_control(p, "param\t", 4)


def p_var_typ(p):
    '''var_typ : INT
               | FLOAT
               | CHAR
               | BOOL
               | FRAME
    '''
    p[0] = p[1]
    # print_control(p, "var_typ", 1)


def p_func_typ(p):
    '''func_typ : INT
                | FLOAT
                | CHAR
                | BOOL
                | FRAME
                | VOID
    '''
    p[0] = p[1]
    p.parser.func_type_read = encode_func_type(p[1])
    print_control(p, "func_typ", 1)


def p_check_aritm_operation(p):
    '''check_aritm_operation :
    '''
    # punto neurálgico sumas-restas
    try:
        # when reducing factor PLUS term | factor MINUS term
        operador = p[-1]
        p.parser.cuads.pilaOperadores.append(ENCODE[operador])
    except:
        # when reducing only term
        pass

    #print("parsed check_aritm_operation", p[-1])


def p_check_aritm(p):
    '''check_aritm : 
    '''
    if p.parser.cuads.pilaOperadores[-1] in [ENCODE['+'], ENCODE['-']]:
        current_func = p.parser.context
        # print(f"{p.parser.cuads.pilaOperadores[-1]} <- haz esto")
        right_operand = p.parser.cuads.pilaOperandos.pop()
        right_type = p.parser.cuads.pilaTipos.pop()
        left_operand = p.parser.cuads.pilaOperandos.pop()
        left_type = p.parser.cuads.pilaTipos.pop()
        operador = p.parser.cuads.pilaOperadores.pop()
        try:
            temp_type = CUBO[operador][left_type][right_type]
        except:
            raise Exception(f"operation {operador} between {left_type} and {right_type} invalid.")
        
        result = p.parser.dir_funcs.funcs[current_func]['vars'].add_temp(temp_type=temp_type)
        p.parser.cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=result)
        p.parser.cuads.pilaOperandos.append(result)
        p.parser.cuads.pilaTipos.append(temp_type)
    else:
        # print("not + nor - on top of the stack")
        pass
    # print("parsed check_aritm")
    

def p_aritm(p):
    '''aritm : term check_aritm PLUS check_aritm_operation aritm
             | term check_aritm MINUS check_aritm_operation aritm
             | term check_aritm
    '''
    try:
        p[0] = f"{p[1]} {p[3]} {p[5]}"
    except: 
        p[0] = p[1]
    print_control(p, "aritm\t", 5)


def p_check_term_operation(p):
    '''check_term_operation :
    '''
    # punto neurálgico mults-divs
    try:
        # when reducing factor TIMES term | factor DIVIDE term
        operador = p[-1]
        p.parser.cuads.pilaOperadores.append(ENCODE[operador])
    except:
        pass
    # print("parsed check_term_operation", p[-1])
    
def p_check_term(p):
    '''check_term :
    '''
    if p.parser.cuads.pilaOperadores[-1] in [ENCODE['*'], ENCODE['/']]:
        current_func = p.parser.context
        # print(f"{p.parser.cuads.pilaOperadores[-1]} <- haz esto")
        right_operand = p.parser.cuads.pilaOperandos.pop()
        right_type = p.parser.cuads.pilaTipos.pop()
        left_operand = p.parser.cuads.pilaOperandos.pop()
        left_type = p.parser.cuads.pilaTipos.pop()
        operador = p.parser.cuads.pilaOperadores.pop()
        try:
            temp_type = CUBO[operador][left_type][right_type]
        except:
            raise Exception(f"operation {operador} between {left_type} and {right_type} invalid.")
        
        result = p.parser.dir_funcs.funcs[current_func]['vars'].add_temp(temp_type=temp_type)
        p.parser.cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=result)
        p.parser.cuads.pilaOperandos.append(result)
        p.parser.cuads.pilaTipos.append(temp_type)
    else:
        # print("not * nor / on top of the stack")
        pass


def p_term(p):
    '''term : factor check_term TIMES check_term_operation term
            | factor check_term DIVIDE check_term_operation term
            | factor check_term
    '''
    try:
        p[0] = p[1,3,5]
    except: 
        p[0] = p[1]
    print_control(p, "term\t", 5)
    

def p_factortype_const_int(p):
    "factortype_const_int : "
    # add factor type to pilaTipos
    p.parser.cuads.pilaTipos.append(ENCODE["int"])


def p_factortype_const_float(p):
    "factortype_const_float : "
    # add factor type to pilaTipos
    p.parser.cuads.pilaTipos.append(ENCODE["float"])
    # print("viene un float")

    
def p_factor_const(p):
    """factor_const : CONST_INT factortype_const_int
                    | CONST_FLOAT factortype_const_float
    """
    print_control(p, "factor_const", 2)
    p[0] = p[1]
    # add factor to pilaOperandos
    p.parser.cuads.pilaOperandos.append(p[1])


def p_factor_var(p):
    """factor_var : ID
                  | ID dims
    """
    p[0] = p[1]
    try:
        # looking for variable in local scope
        current_func = p.parser.context
        type = p.parser.dir_funcs.funcs[current_func]['vars'].vars[p[1]]['tipo']
        
        p[0] = p[1]
        
        # add factor to pilaOperandos
        p.parser.cuads.pilaOperandos.append(p[1])
        # add factor type to pilaTipos
        p.parser.cuads.pilaTipos.append(type)
        
    except:
        try:
            # looking for variable in global scope
            type = p.parser.dir_funcs.funcs[p.parser.programName]['vars'].vars[p[1]]['tipo']
            
            # add factor to pilaOperandos
            p.parser.cuads.pilaOperandos.append(p[1])
            # add factor type to pilaTipos
            p.parser.cuads.pilaTipos.append(type)
        except:
            raise Exception(f"Expression {p[1]} unknown")
        
    print_control(p, "factor_var", 2)


def p_factor_function_call(p):
    """factor_function_call : ID OPPARENTH CLPARENTH
                            | ID OPPARENTH args CLPARENTH
    """
    p[0] = p[1]
    print_control(p, "factor_function_call", 4)

def p_check_parenth(p):
    '''check_parenth : 
    '''
    if p[-1] == "(":
        p.parser.cuads.pilaOperadores.append("(")
    elif p[-1] == ")":
        oper = p.parser.cuads.pilaOperadores.pop()
        if oper != "(":
            raise Exception("Unexpected behaviour, didn't find a (")


def p_factor(p):
    '''factor : OPPARENTH check_parenth aritm CLPARENTH check_parenth
              | factor_function_call
              | factor_var
              | factor_const
    '''
    if p[1] == "(":
        p[0] = p[3]
    else:
        p[0] = p[1]
        
    print_control(p, "factor\t", 3)


def p_relac(p):
    '''relac : aritm EQUAL aritm
             | aritm UNEQUAL aritm
             | aritm LESS aritm
             | aritm LESSEQ aritm
             | aritm GREATER aritm
             | aritm GREATEREQ aritm
    '''
    p.parser.cuads.pilaOperadores.append(ENCODE[p[2]])
    # print(f"{p.parser.cuads.pilaOperadores[-1]} <- haz esto")
    current_func = p.parser.context
    right_operand = p.parser.cuads.pilaOperandos.pop()
    right_type = p.parser.cuads.pilaTipos.pop()
    left_operand = p.parser.cuads.pilaOperandos.pop()
    left_type = p.parser.cuads.pilaTipos.pop()
    operador = p.parser.cuads.pilaOperadores.pop()
    try:
        temp_type = CUBO[operador][left_type][right_type]
    except:
        raise Exception(f"operation {operador} between {left_type} and {right_type} invalid.")
    
    result = p.parser.dir_funcs.funcs[current_func]['vars'].add_temp(temp_type=temp_type)
    p.parser.cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=result)
    p[0] = result
    print_control(p, "relac\t", 3)


def p_args(p):
    '''args : aritm COMMA args
            | aritm
    '''
    print_control(p, "args\t", 3)


def p_lectura(p):
    '''lectura : READ OPPARENTH CLPARENTH
    '''
    # p[0] = float(input())
    
    current_func = p.parser.context
    result = p.parser.dir_funcs.funcs[current_func]['vars'].add_temp(temp_type=ENCODE["float"])
    p.parser.cuads.add_cuadruplo(operation=ENCODE["READ"], result=result)
    
    p.parser.cuads.pilaOperandos.append(result)
    p.parser.cuads.pilaTipos.append(ENCODE["float"])
    print_control(p, "lectura", 3)


def p_escritura(p):
    '''escritura : WRITE OPPARENTH aritm CLPARENTH
                 | WRITE OPPARENTH CONST_STRING CLPARENTH
    '''
    if p.parser.cuads.pilaOperandos[-1] == "$":
        p.parser.cuads.add_cuadruplo(operation=ENCODE["PRINT"], leftOp=p[3])
    else:
        operando = p.parser.cuads.pilaOperandos.pop()
        tipo = p.parser.cuads.pilaTipos.pop()
        p.parser.cuads.add_cuadruplo(operation=ENCODE["PRINT"], leftOp=operando)
        
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
    if p.parser.cuads.pilaOperandos[-1] != "$":
        try:
            # looking for variable in local scope
            current_func = p.parser.context
            type = p.parser.dir_funcs.funcs[current_func]['vars'].vars[p[1]]['tipo']
            
            # # add factor to pilaOperandos
            # p.parser.cuads.pilaOperandos.append(p[1])
            # # add factor type to pilaTipos
            # p.parser.cuads.pilaTipos.append(type)
            
        except:
            try:
                # looking for variable in global scope
                type = p.parser.dir_funcs.funcs[p.parser.programName]['vars'].vars[p[1]]['tipo']
                
                # # add factor to pilaOperandos
                # p.parser.cuads.pilaOperandos.append(p[1])
                # # add factor type to pilaTipos
                # p.parser.cuads.pilaTipos.append(type)
            except:
                raise Exception(f"Expression {p[1]} unknown")
        
        
        operando = p.parser.cuads.pilaOperandos.pop()
        _ = p.parser.cuads.pilaTipos.pop()
        
        p.parser.cuads.add_cuadruplo(operation=ENCODE["ASSIGN"], leftOp=operando, result=p[1])
    else:
        raise Exception("Unexpected behaviour: pilaOperandos is empty")

    print_control(p, "asign\t", 4)
    

#--- END : funciones de la gramática formal ---