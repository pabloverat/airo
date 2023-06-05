# grammar.py

from utils import print_control
from dir_funcs import Dir_Funcs
from tabla_vars import Tabla_Vars
from tabla_consts import Tabla_Consts
from cuadruplos import Cuadruplos
from dim_node import Dim_Node
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
    current_func = p.parser.programName
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
    
    # guardando nombre del programa
    p.parser.programName = "Program"
    
    # guardando nombre de contexto actual
    p.parser.context = p.parser.programName
    
    # creando tabla de variables globales
    globalVars = Tabla_Vars()
    globalVars.vars_range = {
        ENCODE["bool"]:    (11_000, 11_999),
        ENCODE["char"]:    (12_000, 12_999),
        ENCODE["int"]:     (13_000, 13_999),
        ENCODE["float"]:   (14_000, 14_999),
        ENCODE["frame"]:   (15_000, 18_999),
        ENCODE["ptr"]: (19_000, 19_999),
    }
    globalVars.temps_range = {
        ENCODE["bool"]:    (111_000, 111_999),
        # ENCODE["char"]:  (112_000, 112_999),
        ENCODE["int"]:     (113_000, 113_999),
        ENCODE["float"]:   (114_000, 114_999),
        # ENCODE["frame"]: (115_000, 118_999),
        ENCODE["ptr"]: (119_000, 119_999),
    }
    # guardando programa como una función den directorio de funciones
    p.parser.dir_funcs.add_func(func_name=p.parser.programName, func_type=ENCODE["programa"], dir_inicio=1, varTable=globalVars)
    
    # variable para pila de dimensiones para arreglos
    p.parser.DIMS = 1
    
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
    p.parser.cuads.add_cuadruplo(operation=ENCODE['ERA'], leftOp=p.parser.programName)
    p.parser.aux_cuads.add_cuadruplo(operation='ERA', leftOp=p.parser.programName)
    p[0] = "ɛ"
    print("Parsed context_to_global\t")


def p_cuerpo(p):
    '''cuerpo : MAIN context_to_global OPPARENTH CLPARENTH OPBRACE estat_list calcula_globales CLBRACE
    '''
    print_control(p, "cuerpo\t", 8)


def p_variable(p):
    '''variable : VAR ID COLON var_typ
                | VAR ID COLON var_typ declare_dims
    '''
    p[0] = p[2]
    current_func = p.parser.context
    
    try:
        # when dims are declared
        _ = p[5]
        dims = p.parser.temp_dims
        p.parser.temp_dims = None
        p.parser.dir_funcs.funcs[current_func]['varTable'].add_var(p[2], ENCODE[p[4]], dims=dims)
    except:
        # when dims are not declared
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

    lim_inf = p[-4]
    lim_sup = p[-2]
    assert lim_sup>lim_inf, f"ArraysLimitsError: {lim_inf} !< {lim_sup}"
    
    dim1 = Dim_Node(lim_inf=lim_inf, lim_sup=lim_sup)
    dim1.set_values(dim=1)
    m0 = dim1.calc_r()
    dim1.set_values(r=m0)
    m1 = dim1.calc_m(prev_m=m0)
    dim1.set_values(m=m1)
    assert m1 == 1, "ArrayError: m1 not equal to 1"
    offset = dim1.calc_offset()
    dim1.set_values(minus_k=(-1)*offset)
    
    p.parser.temp_dims = dim1
    print("dim1", dim1.to_dict())


def p_save_matrix_size(p):
    '''save_matrix_size : 
    '''
    p[0] = "ɛ"
    current_func = p.parser.context
    
    # Primera dimensión
    lim_inf1 = p[-9]
    lim_sup1 = p[-7]
    assert lim_sup1>lim_inf1, f"ArraysLimitsError: {lim_inf1} !< {lim_sup1}"
    dim1 = Dim_Node(lim_inf=lim_inf1, lim_sup=lim_sup1)
    dim1.set_values(dim=1)
    
    # Segunda dimensión
    lim_inf2 = p[-4]
    lim_sup2 = p[-2]
    assert lim_sup2>lim_inf2, f"MatrixLimitsError: {lim_inf2} !< {lim_sup2}"
    dim2 = Dim_Node(lim_inf=lim_inf2, lim_sup=lim_sup2)
    dim2.set_values(dim=2)
    dim1.set_values(next=dim2)
    dim2.set_values(prev=dim1)
    
    
    r1 = dim1.calc_r()
    dim1.set_values(r=r1)
    m0 = dim2.calc_r()
    dim2.set_values(r=m0)
    m1 = dim1.calc_m(prev_m=m0)
    dim1.set_values(m=m1)
    offset1 = dim1.calc_offset()
    dim1.set_values(offset=offset1)
    m2 = dim2.calc_m(prev_m=m1)
    dim2.set_values(m=m2)
    assert m2 == 1, "MatrixError: m2 not equal to 1"
    offset2 = dim2.calc_offset(prev_offset=offset1)
    dim2.set_values(minus_k=(-1)*offset2)
    
    p.parser.temp_dims = dim1
    print("dim1", dim1.to_dict())
    print("dim2", dim2.to_dict())


def p_declare_dims(p):
    '''declare_dims : OPBRACKET CONST_INT COLON CONST_INT CLBRACKET save_array_size
                    | OPBRACKET CONST_INT COLON CONST_INT CLBRACKET OPBRACKET CONST_INT COLON CONST_INT CLBRACKET save_matrix_size
    '''
    
    try:
        p[0] = f"{p[1]}{p[2]}{p[3]}{p[4]}{p[5]}{p[6]}{p[7]}{p[8]}{p[9]}{p[10]}"
    except:
        p[0] = f"{p[1]}{p[2]}{p[3]}{p[4]}{p[5]}"
        
    print_control(p, "declare_dims\t", 11)


def p_save_array_index(p):
    '''save_array_index : 
    '''
    p[0] = "ɛ"
    # print("save_array_size")


def p_dims_q1(p):
    '''dims_q1 : 
    '''
    print("pOperadores0:", p.parser.cuads.pilaOperadores)
    print("pOperandos0:", p.parser.cuads.pilaOperandos)
    print("pTipos0:", p.parser.cuads.pilaTipos)
    print("DIMS1:", p.parser.DIMS)
    # stashing variable that is trying to be indexed
    print(p.parser.dims_var)
    current_var, var_found = list(p.parser.dims_var.items())[0]

    assert var_found['dims'] is not None, f"variable {current_var} trying to be indexed is not indexable"
    
    p.parser.cuads.pilaDimensiones.append((current_var, p.parser.DIMS))
    # print("pOperadores2:", p.parser.cuads.pilaOperadores)
    p.parser.cuads.pilaOperadores.append("[")
    print("pOperadores2:", p.parser.cuads.pilaOperadores)
    
    p.parser.aux_cuads.pilaDimensiones.append((current_var, p.parser.DIMS))
    p.parser.aux_cuads.pilaOperadores.append("[")


def p_dims_q2(p):
    '''dims_q2 : 
    '''
    current_var, var_found = list(p.parser.dims_var.items())[0]
    if p.parser.DIMS == 1:
        dim_node = var_found['dims']
    elif p.parser.DIMS == 2:
        dim_node = var_found['dims'].next
    else:
        print(p.parser.DIMS)
        raise Exception("dims diff than 1 or 2")

    lim_inf = dim_node.lim_inf
    lim_sup = dim_node.lim_sup

    dim_type = p.parser.cuads.pilaTipos[-1]
    assert dim_type == ENCODE['int'], f"trying to index array with an element of type {dim_type}"
    dim_value = p.parser.cuads.pilaOperandos[-1]

    p.parser.cuads.add_cuadruplo(operation=ENCODE['VERIFY'], leftOp=dim_value, rightOp=lim_inf, result=lim_sup)
    # aux_cuads
    p.parser.aux_cuads.add_cuadruplo(operation='VERIFY', leftOp=dim_value, rightOp=lim_inf, result=lim_sup)
    
    current_func = p.parser.context
    
    print("DIMS2:", p.parser.DIMS)
    if dim_node.next:
        print("pOperandos1:", p.parser.cuads.pilaOperandos)
        print("pTipos1:", p.parser.cuads.pilaTipos)
        aux = p.parser.cuads.pilaOperandos.pop()
        aux_type = p.parser.cuads.pilaTipos.pop()
        print("pOperandos1.2:", p.parser.cuads.pilaOperandos)
        print("pTipos1.2:", p.parser.cuads.pilaTipos)
        m = dim_node.m
        m_address = p.parser.const_table.add_const(const=m, type=ENCODE['float'])
        
        temp_name, temp_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(temp_type=ENCODE['float'])
        p.parser.cuads.add_cuadruplo(operation=ENCODE['*'], leftOp=aux, rightOp=m_address, result=temp_address)
        p.parser.cuads.pilaOperandos.append(temp_address)
        print("pOperandos1.5:", p.parser.cuads.pilaOperandos)
        print("pTipos1.5:", p.parser.cuads.pilaTipos)
        # aux_cuads
        aux = p.parser.aux_cuads.pilaOperandos.pop()
        # aux_type = p.parser.aux_cuads.pilaTipos.pop()
        p.parser.aux_cuads.add_cuadruplo(operation='*', leftOp=aux, rightOp=m, result=temp_name)
        p.parser.aux_cuads.pilaOperandos.append(temp_name)


    if p.parser.DIMS == 2:
        aux2 = p.parser.cuads.pilaOperandos.pop()
        # aux2_type = p.parser.cuads.pilaTipos.pop()
        aux1 = p.parser.cuads.pilaOperandos.pop()
        # aux1_type = p.parser.cuads.pilaTipos.pop()
        temp_name, temp_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(temp_type=ENCODE['float'])
        p.parser.cuads.add_cuadruplo(operation=ENCODE['+'], leftOp=aux1, rightOp=aux2, result=temp_address)
        p.parser.cuads.pilaOperandos.append(temp_address)
        print("pOperandos2.5:", p.parser.cuads.pilaOperandos)
        print("pTipos2:", p.parser.cuads.pilaTipos)
        # aux_cuads
        aux2 = p.parser.aux_cuads.pilaOperandos.pop()
        # aux2_type = p.parser.aux_cuads.pilaTipos.pop()
        aux1 = p.parser.aux_cuads.pilaOperandos.pop()
        # aux1_type = p.parser.aux_cuads.pilaTipos.pop()
        p.parser.aux_cuads.add_cuadruplo(operation='+', leftOp=aux1, rightOp=aux2, result=temp_name)
        p.parser.aux_cuads.pilaOperandos.append(temp_name)


    p.parser.DIMS += 1
    _ = p.parser.cuads.pilaDimensiones.pop()
    p.parser.cuads.pilaDimensiones.append((current_var, p.parser.DIMS))
    
    _ = p.parser.aux_cuads.pilaDimensiones.pop()
    p.parser.aux_cuads.pilaDimensiones.append((current_var, p.parser.DIMS))
    
    


def p_dims(p):
    '''dims : OPBRACKET dims_q1 aritm dims_q2 CLBRACKET
            | OPBRACKET dims_q1 aritm dims_q2 CLBRACKET OPBRACKET aritm dims_q2 CLBRACKET
    '''
    
    current_func = p.parser.context
    current_var, var_found = list(p.parser.dims_var.items())[0]
    
    aux1 = p.parser.cuads.pilaOperandos.pop()
    print("DIMS3:", p.parser.DIMS)
    # sumando -k
    minus_k = var_found['dims'].next.minus_k if p.parser.DIMS == 3 else var_found['dims'].minus_k
    minus_k_address = p.parser.const_table.add_const(const=minus_k, type=ENCODE['int'])
    tempi_name, tempi_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(ENCODE['float'])
    p.parser.cuads.add_cuadruplo(operation=ENCODE['+'], leftOp=aux1, rightOp=minus_k_address, result=tempi_address)
    # sumando dirección base
    base_dir = var_found['address']
    base_dir_address = p.parser.const_table.add_const(const=base_dir, type=ENCODE['int'])
    tempn_name, tempn_address = p.parser.dir_funcs.funcs[p.parser.dims_var_scope]['varTable'].add_temp(ENCODE['ptr'])
    p.parser.cuads.add_cuadruplo(operation=ENCODE['+'], leftOp=tempi_address, rightOp=base_dir_address, result=tempn_address)    
    p.parser.cuads.pilaOperandos.append(tempn_address)
    print("pOperandos3:", p.parser.cuads.pilaOperandos)
    print("pTipos3:", p.parser.cuads.pilaTipos)

    # aux_cuads
    aux1 = p.parser.aux_cuads.pilaOperandos.pop()
    p.parser.aux_cuads.add_cuadruplo(operation='+', leftOp=aux1, rightOp=minus_k, result=tempi_name)
    # _, temp_address = p.parser.dir_funcs.funcs[current_func]['varTable'].add_temp(ENCODE['ptr'])
    p.parser.aux_cuads.add_cuadruplo(operation='+', leftOp=tempi_name, rightOp=base_dir, result=tempn_name)
    p.parser.aux_cuads.pilaOperandos.append(tempn_name)
    
    
    
    assert p.parser.cuads.pilaOperadores[-1] == "[", "ArrayError: something left in pilaOperadores when closing array indexing"
    _ = p.parser.cuads.pilaOperadores.pop()
    _ = p.parser.aux_cuads.pilaOperadores.pop()
        
    p.parser.DIMS = 1
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
        
    # agregar tipo de función a dir_funcs   
    p.parser.dir_funcs.funcs[func_name]['func_type'] = ENCODE[func_type]
    
    # si la función tiene return, agregar una variable global son su nombre
    if func_type not in ['void']:
        p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].add_var(var_name=func_name, var_type=ENCODE[func_type])
        p.parser.dir_funcs.funcs[func_name]['return_address'] = p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].vars[func_name]['address']
    
    p[0] = "ɛ"
    print("save_global_func")


def p_func(p):
    '''func : FUNC ID context_to_local OPPARENTH CLPARENTH COLON func_typ save_global_func OPBRACE func_cont CLBRACE
            | FUNC ID context_to_local OPPARENTH param_list CLPARENTH COLON func_typ save_global_func OPBRACE func_cont CLBRACE
    '''
    func_name = p[2]
    
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
    return_value = p.parser.cuads.pilaOperandos.pop()
    return_type = p.parser.cuads.pilaTipos.pop()
    current_func = p.parser.context
    function_type = p.parser.dir_funcs.funcs[current_func]['func_type']

    if function_type != return_type:
        raise Exception(f"return type {DECODE[return_type]} mismatch with function type {DECODE[function_type]}")

    p.parser.cuads.add_cuadruplo(operation=ENCODE['RETURN'], leftOp=return_value)
    
    return_value = p.parser.aux_cuads.pilaOperandos.pop()
    return_type = p.parser.aux_cuads.pilaTipos.pop()
    p.parser.aux_cuads.add_cuadruplo(operation='RETURN', leftOp=return_value)
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


def p_save_dims_var(p):
    '''save_dims_var : 
    '''
    # stashing variable that is trying to be indexed
    if p[-2] == ":":
        # variable trying to be indexed is being passed as parameter
        current_var = p[-3]
    else:
        current_var = p[-1]

    # looking for variable in varTables
    current_func = p.parser.context
    if current_var in p.parser.dir_funcs.funcs[current_func]['varTable'].vars.keys():
        # looking for variable in local scope
        p.parser.dims_var_scope = current_func
        p.parser.dims_var = {k:v for k,v in p.parser.dir_funcs.funcs[current_func]['varTable'].vars.items() if current_var == k}
    elif current_var in p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].vars.keys():
        # looking for variable in global scope
        p.parser.dims_var_scope = p.parser.programName
        p.parser.dims_var = {k:v for k,v in p.parser.dir_funcs.funcs[p.parser.programName]['varTable'].vars.items() if current_var == k}
    else:
        raise Exception(f"Expression {current_var} unknown")
        

def p_param(p):
    '''param : ID COLON var_typ
             | ID COLON var_typ save_dims_var dims
    '''
    p[0] = p[1]
    current_func = p.parser.context
    p.parser.dir_funcs.funcs[current_func]['varTable'].add_var(p[1], ENCODE[p[3]])
    p.parser.dir_funcs.funcs[current_func]['params'] = p.parser.dir_funcs.funcs[current_func]['params']+[ENCODE[p[3]]]    
    param_address = p.parser.dir_funcs.funcs[current_func]['varTable'].vars[p[1]]['address']
    p.parser.dir_funcs.funcs[current_func]['params_addresses'] = p.parser.dir_funcs.funcs[current_func]['params_addresses']+[param_address]
    print_control(p, "param\t", 5)


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
                  | ID save_dims_var dims
    """
    p[0] = p[1]
    try:
        # for arrays and matrices
        _ = p[3]
    except:
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
    
    p.parser.cuads.pilaOperadores.append("(")
    p.parser.aux_cuads.pilaOperadores.append("(")
    
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
    
    oper = p.parser.cuads.pilaOperadores.pop()
    oper = p.parser.aux_cuads.pilaOperadores.pop()
    if oper != "(":
        raise Exception("Unexpected behaviour, didn't find a (")
    
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
        print("pOperandos23:", p.parser.cuads.pilaOperandos)
        print("pTipos23:", p.parser.cuads.pilaTipos)
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
             | ID save_dims_var dims ASGNMNT lectura
             | ID save_dims_var dims ASGNMNT aritm
             | ID save_dims_var dims ASGNMNT CONST_STRING add_string_const
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
        
        print("pOperandos8:", p.parser.cuads.pilaOperandos)
        print("Tipos8:", p.parser.cuads.pilaTipos)
        operando = p.parser.cuads.pilaOperandos.pop()
        operando_type = p.parser.cuads.pilaTipos.pop()        
        if operando_type != var_found['tipo']:
            raise Exception(f"assigning {DECODE[operando_type]} to a variable of type {DECODE[var_found['tipo']]}")
        
        try:
            # for arrays and matrices
            _ = p[5]
            ptr_address = p.parser.cuads.pilaOperandos.pop()
            print("pOperandos9:", p.parser.cuads.pilaOperandos)
            _ = p.parser.cuads.pilaTipos.pop()
            print("ptr_address:", ptr_address)
            p.parser.cuads.add_cuadruplo(operation=ENCODE["ASSIGN"], leftOp=operando, result=ptr_address)
            print("got here")
        except:
            # for normal vars
            p.parser.cuads.add_cuadruplo(operation=ENCODE["ASSIGN"], leftOp=operando, result=var_found['address'])
        
        operando = p.parser.aux_cuads.pilaOperandos.pop()
        _ = p.parser.aux_cuads.pilaTipos.pop()
        p.parser.aux_cuads.add_cuadruplo(operation="=", leftOp=operando, result=p[1])
    else:
        raise Exception("Unexpected behaviour: pilaOperandos is empty")

    print_control(p, "asign\t", 4)

#--- END : funciones de la gramática formal ---