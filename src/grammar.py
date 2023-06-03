# grammar.py

from utils import print_control
from dir_funcs import Dir_Funcs
from tabla_vars import Tabla_Vars
from tabla_consts import Tabla_Consts
from cuadruplos import Cuadruplos
from cubo import ENCODE, DECODE, CUBO

#--- START : funciones de la gramática formal ---

def p_start(p):
    '''program : encabezamiento var_list func_list cuerpo
               | encabezamiento var_list cuerpo
               | encabezamiento func_list cuerpo
               | encabezamiento cuerpo
    '''
    p[0] = "start"
    print_control(p, "S\t", 5)
    # DELETE DIR_FUNC AND GLOBAL VAR_TABLE
    

def p_calcula_globales(p):
    '''calcula_globales :
    '''
    current_func = p.parser.context
    recursos = p.parser.dir_funcs.funcs[current_func]['varTable'].calculate_resources()
    p.parser.dir_funcs.funcs[current_func]['recursos'] = recursos
    p[0] = "calcula_globales"
    print("Parsed calcula_globales")


def p_encabezamiento(p):
    '''encabezamiento : PROGRAM ID
    '''
    # create dirFunc
    p.parser.dir_funcs = Dir_Funcs()
    # create cuadruplos list
    p.parser.cuads = Cuadruplos()
    p.parser.aux_cuads = Cuadruplos()
    
    # creando tabla de constantes
    p.parser.const_table = Tabla_Consts()
    
    # guardando nombre de contexto actual
    p.parser.context = p[2]
    # guardando nombre del programa
    p.parser.programName = p.parser.context
    
    # creando tabla de variables globales
    globalVars = Tabla_Vars()
    globalVars.vars_range = {
        ENCODE["bool"]:  (11_000, 11_999),
        ENCODE["char"]:  (12_000, 12_999),
        ENCODE["int"]:   (13_000, 14_999),
        ENCODE["float"]: (14_000, 14_999),
        ENCODE["frame"]: (15_000, 19_999),
    }
    globalVars.temps_range = {
        ENCODE["bool"]:  (111_000, 111_999),
        # ENCODE["char"]:  (112_000, 112_999),
        ENCODE["int"]:   (113_000, 114_999),
        ENCODE["float"]: (114_000, 114_999),
        # ENCODE["frame"]: (115_000, 119_999),
    }
    # guardando programa como una función den directorio de funciones
    p.parser.dir_funcs.add_func(func_name=p.parser.context, func_type=ENCODE["programa"], dir_inicio=1, varTable=globalVars)
    
    # generar primer cuadruplo "go to main"
    p.parser.cuads.add_cuadruplo(operation=ENCODE['GOTO'])
    p.parser.aux_cuads.add_cuadruplo(operation='GOTO')
    
    print_control(p, "encabezamiento", 2)


def p_context_to_global(p):
    "context_to_global : "
    p.parser.context = p.parser.programName
    current_cuad = len(p.parser.cuads.cuadruplos)
    p.parser.cuads.cuadruplos[0].result = current_cuad
    p.parser.aux_cuads.cuadruplos[0].result = current_cuad
    p.parser.cuads.add_cuadruplo(operation=ENCODE['ERA'], leftOp=p.parser.context)
    p.parser.aux_cuads.add_cuadruplo(operation='ERA', leftOp=p.parser.context)
    p[0] = "ɛ"
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
    p.parser.dir_funcs.funcs[current_func]['varTable'].add_var(p[2], ENCODE[p[4]])
    print_control(p, "var\t", 5)


def p_var_list(p):
    '''var_list : variable var_list
                | variable
    '''
    try:
        p[0] = f"{p[1]}\t{p[2]}"
    except:
        p[0] = p[1]
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
    p[0] = "ɛ"
    _ = p.parser.cuads.pilaOperandos.pop()
    _ = p.parser.cuads.pilaTipos.pop()
    
    _ = p.parser.aux_cuads.pilaOperandos.pop()
    _ = p.parser.aux_cuads.pilaTipos.pop()
    # print("save_array_size")


def p_dims(p):
    '''dims : OPBRACKET aritm save_array_size CLBRACKET
            | OPBRACKET aritm save_array_size CLBRACKET OPBRACKET aritm save_array_size CLBRACKET
    '''
    try:
        p[0] = f"{p[1]}{p[2]}{p[4]}{p[5]}{p[6]}{p[8]}"
    except:
        p[0] = f"{p[1]}{p[2]}{p[4]}"
    print_control(p, "dims\t", 8)
    
    
def p_save_global_func(p):
    '''save_global_func :
    '''
    func_name = p[-6] if p[-6] != "ɛ" else p[-7]
    func_type = p[-1]
    
    print(func_name, ":", func_type)
    
    # si la función tiene return, agregar una variable global son su nombre
    if func_type not in ['void']:
        p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].add_var(var_name=func_name, var_type=ENCODE[func_type])    
    
    p[0] = "ɛ"
    print("save_global_func")


def p_func(p):
    '''func : FUNC ID context_to_local OPPARENTH CLPARENTH COLON func_typ save_global_func OPBRACE func_cont CLBRACE
            | FUNC ID context_to_local OPPARENTH param_list CLPARENTH COLON func_typ save_global_func OPBRACE func_cont CLBRACE
    '''
    func_name = p[2]
    # p[0] = func_name
    
    # agregar tipo de función
    func_type = p[7] if p[7] != ':' else p[8]
    p.parser.dir_funcs.funcs[func_name]['func_type'] = ENCODE[func_type]
    
    # agregar recursos utilizados por función
    recursos = p.parser.dir_funcs.funcs[func_name]['varTable'].calculate_resources()
    p.parser.dir_funcs.funcs[func_name]['recursos'] = recursos
    
    # generar cuádruplo de ENDFUNC
    p.parser.cuads.add_cuadruplo(operation=ENCODE["ENDFUNC"], leftOp=p.parser.context)
    p.parser.aux_cuads.add_cuadruplo(operation="ENDFUNC", leftOp=p.parser.context)
    
    print_control(p, "func\t", 12)


def p_context_to_local(p):
    "context_to_local :"
    p.parser.context = p[-1]
    func_name = p[-1] 
    
    # check if the function's name is already used
    if func_name in p.parser.dir_funcs.funcs.keys():
        raise Exception(f"func {func_name} already exists")
    
    funcVars = Tabla_Vars()
    dir_inicio = len(p.parser.cuads.cuadruplos)
    p.parser.dir_funcs.add_func(func_name=p.parser.context, func_type=None, dir_inicio=dir_inicio, varTable=funcVars)
    p[0] = "ɛ"
    print("Parsed context_to_local\t")


def p_ciclo_q1(p):
    '''ciclo_q1 : 
    '''
    p.parser.cuads.pilaSaltos.append(len(p.parser.cuads.cuadruplos))
    p.parser.aux_cuads.pilaSaltos.append(len(p.parser.aux_cuads.cuadruplos))
    p[0] = "ɛ"

    
def p_ciclo_q2(p):
    '''ciclo_q2 :
    '''
    end = p.parser.cuads.pilaSaltos.pop()
    ret = p.parser.cuads.pilaSaltos.pop()
    p.parser.cuads.add_cuadruplo(operation=ENCODE["GOTO"], result=ret)
    p.parser.cuads.cuadruplos[end-1].result = len(p.parser.cuads.cuadruplos)
    
    end = p.parser.aux_cuads.pilaSaltos.pop()
    ret = p.parser.aux_cuads.pilaSaltos.pop()
    p.parser.aux_cuads.add_cuadruplo(operation="GOTO", result=ret)
    p.parser.aux_cuads.cuadruplos[end-1].result = len(p.parser.aux_cuads.cuadruplos)
    p[0] = "ɛ"
        

def p_ciclo(p):
    '''ciclo : WHILE ciclo_q1 OPPARENTH relac conditional_q1 CLPARENTH THEN OPBRACE estat_list CLBRACE ciclo_q2
    '''
    print_control(p, "ciclo\t", 8)


def p_conditional_q1(p):
    '''conditional_q1 : 
    '''
    p.parser.cuads.add_cuadruplo(operation=ENCODE["GOTOF"], leftOp=p[-1])
    p.parser.cuads.pilaSaltos.append(len(p.parser.cuads.cuadruplos))
    
    p.parser.aux_cuads.add_cuadruplo(operation="GOTOF", leftOp=p[-1])
    p.parser.aux_cuads.pilaSaltos.append(len(p.parser.aux_cuads.cuadruplos))
    p[0] = "ɛ"


def p_conditional_q2(p):
    '''conditional_q2 : 
    '''
    else_cuad = len(p.parser.cuads.cuadruplos)
    gotof_cuad = p.parser.cuads.pilaSaltos.pop()
    p.parser.cuads.cuadruplos[gotof_cuad-1].result = else_cuad
    
    else_cuad = len(p.parser.aux_cuads.cuadruplos)
    gotof_cuad = p.parser.aux_cuads.pilaSaltos.pop()
    p.parser.aux_cuads.cuadruplos[gotof_cuad-1].result = else_cuad
    p[0] = "ɛ"

    
def p_conditional_q3(p):
    '''conditional_q3 : 
    '''
    p.parser.cuads.add_cuadruplo(operation=ENCODE["GOTO"])
    false = p.parser.cuads.pilaSaltos.pop()
    p.parser.cuads.pilaSaltos.append(len(p.parser.cuads.cuadruplos))
    p.parser.cuads.cuadruplos[false-1].result = len(p.parser.cuads.cuadruplos)
    
    p.parser.aux_cuads.add_cuadruplo(operation="GOTO")
    false = p.parser.aux_cuads.pilaSaltos.pop()
    p.parser.aux_cuads.pilaSaltos.append(len(p.parser.aux_cuads.cuadruplos))
    p.parser.aux_cuads.cuadruplos[false-1].result = len(p.parser.aux_cuads.cuadruplos)
    p[0] = "ɛ"
    

def p_decision(p):
    '''decision : WHEN OPPARENTH relac conditional_q1 CLPARENTH THEN OPBRACE estat_list CLBRACE conditional_q2
                | WHEN OPPARENTH relac conditional_q1 CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE conditional_q3 OPBRACE estat_list CLBRACE conditional_q2
    '''
    print_control(p, "decision", 16 )


def p_save_return_value(p):
    '''save_return_value :
    '''
    returnValue = p.parser.cuads.pilaOperandos.pop()
    returnType = p.parser.cuads.pilaTipos.pop()
    
    returnValue = p.parser.aux_cuads.pilaOperandos.pop()
    returnType = p.parser.aux_cuads.pilaTipos.pop()
    p[0] = "ɛ"


def p_func_cont(p):
    '''func_cont : var_list estat_list RETURN aritm save_return_value
                 | estat_list RETURN aritm save_return_value
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
                | ID ASGNMNT LOAD OPPARENTH CONST_STRING add_string_const CLPARENTH 
    '''
    print_control(p, "carga_dt", 6)


def p_param(p):
    '''param : ID COLON var_typ
             | ID COLON var_typ dims
    '''
    p[0] = p[1]
    current_func = p.parser.context
    p.parser.dir_funcs.funcs[current_func]['varTable'].add_var(p[1], ENCODE[p[3]])
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


def p_func_typ(p):
    '''func_typ : INT
                | FLOAT
                | CHAR
                | BOOL
                | FRAME
                | VOID
    '''
    p[0] = p[1]
    print_control(p, "func_typ", 1)


def p_check_aritm_operation(p):
    '''check_aritm_operation :
    '''
    # punto neurálgico sumas-restas
    try:
        # when reducing factor PLUS term | factor MINUS term
        operador = p[-1]
        p.parser.cuads.pilaOperadores.append(ENCODE[operador])
        p.parser.aux_cuads.pilaOperadores.append(operador)
    except:
        # when reducing only term
        pass

    p[0] = "ɛ"


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
            raise Exception(f"operation {DECODE[operador]} between {DECODE[left_type]} and {DECODE[right_type]} invalid.")
        
        temp_name, temp_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(temp_type=temp_type)
        p.parser.cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=temp_address)
        p.parser.cuads.pilaOperandos.append(temp_address)
        p.parser.cuads.pilaTipos.append(temp_type)
        
        
        right_operand = p.parser.aux_cuads.pilaOperandos.pop()
        right_type = p.parser.aux_cuads.pilaTipos.pop()
        left_operand = p.parser.aux_cuads.pilaOperandos.pop()
        left_type = p.parser.aux_cuads.pilaTipos.pop()
        operador = p.parser.aux_cuads.pilaOperadores.pop()
        p.parser.aux_cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=temp_name)
        p.parser.aux_cuads.pilaOperandos.append(temp_name)
        p.parser.aux_cuads.pilaTipos.append(temp_type)
    else:
        # print("not + nor - on top of the stack")
        pass
    p[0] = "ɛ"
    

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
        p.parser.aux_cuads.pilaOperadores.append(operador)
    except:
        pass

    p[0] = "ɛ"

    
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
            raise Exception(f"operation {DECODE[operador]} between {DECODE[left_type]} and {DECODE[right_type]} invalid.")
        
        temp_name, temp_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(temp_type=temp_type)
        p.parser.cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=temp_address)
        p.parser.cuads.pilaOperandos.append(temp_address)
        p.parser.cuads.pilaTipos.append(temp_type)
        
        
        right_operand = p.parser.aux_cuads.pilaOperandos.pop()
        right_type = p.parser.aux_cuads.pilaTipos.pop()
        left_operand = p.parser.aux_cuads.pilaOperandos.pop()
        left_type = p.parser.aux_cuads.pilaTipos.pop()
        operador = p.parser.aux_cuads.pilaOperadores.pop()
        p.parser.aux_cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=temp_name)
        p.parser.aux_cuads.pilaOperandos.append(temp_name)
        p.parser.aux_cuads.pilaTipos.append(temp_type)
    else:
        # print("not * nor / on top of the stack")
        pass
    
    p[0] = "ɛ"


def p_term(p):
    '''term : factor check_term TIMES check_term_operation term
            | factor check_term DIVIDE check_term_operation term
            | factor check_term
    '''
    try:
        p[0] = f"{p[1]} {p[3]} {p[5]}"
    except: 
        p[0] = p[1]

    print_control(p, "term\t", 5)
    

def p_factortype_const_int(p):
    "factortype_const_int : "
    # add factor type to pilaTipos
    p.parser.cuads.pilaTipos.append(ENCODE["int"])
    # add factor_const to const_table
    const_address = p.parser.const_table.add_const(const=p[-1], type=ENCODE["int"])
    # add factor to pilaOperandos
    p.parser.cuads.pilaOperandos.append(const_address)
    
    p.parser.aux_cuads.pilaTipos.append(ENCODE["int"])
    p.parser.aux_cuads.pilaOperandos.append(p[-1])
    
    p[0] = "ɛ"


def p_factortype_const_float(p):
    "factortype_const_float : "
    # add factor type to pilaTipos
    p.parser.cuads.pilaTipos.append(ENCODE["float"])
    # add factor_const to const_table
    const_address = p.parser.const_table.add_const(const=p[-1], type=ENCODE["float"])
    # add factor to pilaOperandos
    p.parser.cuads.pilaOperandos.append(const_address)
    
    p.parser.aux_cuads.pilaTipos.append(ENCODE["float"])
    p.parser.aux_cuads.pilaOperandos.append(p[-1])
    
    p[0] = "ɛ"

    
def p_factor_const(p):
    """factor_const : CONST_INT factortype_const_int
                    | CONST_FLOAT factortype_const_float
    """
    p[0] = p[1]
    print_control(p, "factor_const", 2)


def p_factor_var(p):
    """factor_var : ID
                  | ID dims
    """
    p[0] = p[1]
    try:
        # looking for variable in local scope
        current_func = p.parser.context
        var_found = p.parser.dir_funcs.funcs[current_func]['varTable'].vars[p[1]]#['address']
        
        p[0] = p[1]
        
        # add factor to pilaOperandos
        p.parser.cuads.pilaOperandos.append(var_found['address'])
        # add factor type to pilaTipos
        p.parser.cuads.pilaTipos.append(var_found['tipo'])
        
        p.parser.aux_cuads.pilaOperandos.append(p[1])
        p.parser.aux_cuads.pilaTipos.append(var_found['tipo'])
        
    except:
        try:
            # looking for variable in global scope
            var_found = p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].vars[p[1]]#['tipo']
            
            # add factor to pilaOperandos
            p.parser.cuads.pilaOperandos.append(var_found['address'])
            # add factor type to pilaTipos
            p.parser.cuads.pilaTipos.append(var_found['tipo'])
        
            p.parser.aux_cuads.pilaOperandos.append(p[1])
            p.parser.aux_cuads.pilaTipos.append(var_found['tipo'])
            
        except:
            raise Exception(f"Expression {p[1]} unknown")
        
    print_control(p, "factor_var", 2)


def p_function_call_q1(p):
    '''function_call_q1 :
    '''
    assert p[-2] in p.parser.dir_funcs.funcs.keys(), f"function {p[-2]} unknown"
    p.parser.cuads.add_cuadruplo(operation=ENCODE["ERA"], leftOp=p[-2])
    p.parser.funcCall = p[-2]
    p.parser.paramsK = 0
    p.parser.aux_cuads.add_cuadruplo(operation="ERA", leftOp=p[-2])
    p[0] = "ɛ"


def p_function_call_q2(p):
    '''function_call_q2 :
    '''
    try:
        _ = p.parser.dir_funcs.funcs[p.parser.funcCall]['params'][p.parser.paramsK]
        raise Exception(f"missing arguments in call to {p.parser.funcCall}")
    except:
        pass
    
    dirInicio = p.parser.dir_funcs.funcs[p.parser.funcCall]['dir_inicio']
    p.parser.cuads.add_cuadruplo(operation=ENCODE["GOSUB"], leftOp=p.parser.funcCall, result=dirInicio)
    p.parser.aux_cuads.add_cuadruplo(operation="GOSUB", leftOp=p.parser.funcCall, result=dirInicio)
    p[0] = "ɛ"  


def p_factor_function_call(p):
    """factor_function_call : ID OPPARENTH function_call_q1 CLPARENTH function_call_q2
                            | ID OPPARENTH function_call_q1 args CLPARENTH function_call_q2
    """
    try: 
        func_var = p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].vars[p[1]]
    except:
        raise Exception("func not found in global vars")
    
    p.parser.cuads.pilaOperandos.append(func_var['address'])
    p.parser.cuads.pilaTipos.append(func_var['tipo'])
    # print("pOperandos", p.parser.cuads.pilaOperandos)
    # print("pTipos", p.parser.cuads.pilaTipos)
    
    p.parser.aux_cuads.pilaOperandos.append(p[1])
    p.parser.aux_cuads.pilaTipos.append(func_var['tipo'])
    p[0] = p[1]
    print_control(p, "factor_function_call", 6)
    

def p_check_parenth(p):
    '''check_parenth : 
    '''
    if p[-1] == "(":
        p.parser.cuads.pilaOperadores.append("(")
        p.parser.aux_cuads.pilaOperadores.append("(")
    elif p[-1] == ")":
        oper = p.parser.cuads.pilaOperadores.pop()
        oper = p.parser.aux_cuads.pilaOperadores.pop()
        if oper != "(":
            raise Exception("Unexpected behaviour, didn't find a (")
    
    p[0] = "ɛ"


def p_factor(p):
    '''factor : OPPARENTH check_parenth aritm CLPARENTH check_parenth
              | factor_function_call
              | factor_var
              | factor_const
    '''
    if p[1] == "(":
        p[0] = f"({p[3]})"
    else:
        p[0] = p[1]
        
    print_control(p, "factor\t", 5)


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
        raise Exception(f"operation {DECODE[operador]} between {DECODE[left_type]} and {DECODE[right_type]} invalid.")
    
    temp_name, temp_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(temp_type=temp_type)
    p.parser.cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=temp_address)
    
    
    p.parser.aux_cuads.pilaOperadores.append(p[2])
    right_operand = p.parser.aux_cuads.pilaOperandos.pop()
    right_type = p.parser.aux_cuads.pilaTipos.pop()
    left_operand = p.parser.aux_cuads.pilaOperandos.pop()
    left_type = p.parser.aux_cuads.pilaTipos.pop()
    operador = p.parser.aux_cuads.pilaOperadores.pop()
    p.parser.aux_cuads.add_cuadruplo(operation=operador, leftOp=left_operand, rightOp=right_operand, result=temp_name)
    
    p[0] = temp_address
    print_control(p, "relac\t", 3)


def p_arg_q1(p):
    '''arg_q1 :
    '''
    arg = None
    arg = p.parser.cuads.pilaOperandos.pop()
    argType = p.parser.cuads.pilaTipos.pop()

    try:
        paramType = p.parser.dir_funcs.funcs[p.parser.funcCall]['params'][p.parser.paramsK]
        assert argType == paramType, f"argType mismatch paramType: {DECODE[argType]} != {DECODE[paramType]}"
    except:
        raise Exception(f"error in call to {p.parser.funcCall}")
    
    p.parser.cuads.add_cuadruplo(operation=ENCODE["PARAM"], leftOp=arg, rightOp=p.parser.paramsK)
    
    arg = p.parser.aux_cuads.pilaOperandos.pop()
    argType = p.parser.aux_cuads.pilaTipos.pop()
    p.parser.aux_cuads.add_cuadruplo(operation="PARAM", leftOp=arg, rightOp=p.parser.paramsK)
    p[0] = "ɛ"
    
def p_arg_q2(p):
    '''arg_q2 :
    '''
    p.parser.paramsK += 1
    p[0] = "ɛ"


def p_args(p):
    '''args : aritm arg_q1 COMMA arg_q2 args
            | aritm arg_q1
    '''
    try:
        p[0] = f"{p[1]}, {p[5]}"
    except:
        p[0] = p[1]
    print_control(p, "args\t", 5)


def p_lectura(p):
    '''lectura : READ OPPARENTH CLPARENTH
    '''
    p[0] = p[1]
    
    current_func = p.parser.context
    # result = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(temp_type=ENCODE["float"])
    temp_name, temp_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(temp_type=ENCODE["float"])
    p.parser.cuads.add_cuadruplo(operation=ENCODE["READ"], result=temp_address)
    p.parser.cuads.pilaOperandos.append(temp_address)
    p.parser.cuads.pilaTipos.append(ENCODE["float"])
    
    p.parser.aux_cuads.add_cuadruplo(operation="READ", result=temp_name)
    p.parser.aux_cuads.pilaOperandos.append(temp_name)
    p.parser.aux_cuads.pilaTipos.append(ENCODE["float"])
    print_control(p, "lectura", 3)


def p_escritura(p):
    '''escritura : WRITE OPPARENTH aritm CLPARENTH
                 | WRITE OPPARENTH CONST_STRING add_string_const CLPARENTH
    '''
    if p.parser.cuads.pilaOperandos[-1] == "$":
        # si no hay nada en la pila de operandos entonces se está usando la segunda regla
        p.parser.cuads.add_cuadruplo(operation=ENCODE["PRINT"], leftOp=p[4])
        p.parser.aux_cuads.add_cuadruplo(operation="PRINT", leftOp=p[3])
    else:
        operando = p.parser.cuads.pilaOperandos.pop()
        tipo = p.parser.cuads.pilaTipos.pop()
        p.parser.cuads.add_cuadruplo(operation=ENCODE["PRINT"], leftOp=operando)
        
        operando = p.parser.aux_cuads.pilaOperandos.pop()
        tipo = p.parser.aux_cuads.pilaTipos.pop()
        p.parser.aux_cuads.add_cuadruplo(operation="PRINT", leftOp=operando)
    
    p[0] = p[1]
    print_control(p, "escritura", 5)


def p_llam_void(p):
    '''llam_void : ID OPPARENTH function_call_q1 CLPARENTH function_call_q2
                 | ID OPPARENTH function_call_q1 args CLPARENTH function_call_q2
    '''
    print_control(p, "llam_void", 4)

def p_add_string_const(p):
    '''add_string_const : 
    '''
    # add factor_const to const_table
    const_address = p.parser.const_table.add_const(const=p[-1], type=ENCODE["string"])
    p[0] = const_address


def p_asign(p):
    '''asign : ID ASGNMNT lectura
             | ID ASGNMNT aritm
             | ID ASGNMNT CONST_STRING add_string_const
             | ID dims ASGNMNT lectura
             | ID dims ASGNMNT aritm
             | ID dims ASGNMNT CONST_STRING add_string_const
    '''
    if p.parser.cuads.pilaOperandos[-1] != "$":
        try:
            # looking for variable in local scope
            current_func = p.parser.context
            var_found = p.parser.dir_funcs.funcs[current_func]['varTable'].vars[p[1]]
            
        except:
            try:
                # looking for variable in global scope
                var_found = p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].vars[p[1]]

            except:
                raise Exception(f"Expression {p[1]} unknown")
        
        operando = p.parser.cuads.pilaOperandos.pop()
        operando_type = p.parser.cuads.pilaTipos.pop()        
        if operando_type != var_found['tipo']:
            raise Exception(f"assigning {DECODE[operando_type]} to a variable of type {DECODE[var_found['tipo']]}")
        p.parser.cuads.add_cuadruplo(operation=ENCODE["ASSIGN"], leftOp=operando, result=var_found['address'])
        
        operando = p.parser.aux_cuads.pilaOperandos.pop()
        _ = p.parser.aux_cuads.pilaTipos.pop()
        p.parser.aux_cuads.add_cuadruplo(operation="=", leftOp=operando, result=p[1])
    else:
        raise Exception("Unexpected behaviour: pilaOperandos is empty")

    print_control(p, "asign\t", 4)
    

#--- END : funciones de la gramática formal ---