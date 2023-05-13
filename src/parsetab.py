
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ASGNMNT BOOL CHAR CLBRACE CLBRACKET CLPARENTH COLON COMMA CONST_FLOAT CONST_INT CONST_STRING DIVIDE ELSE EQUAL FLOAT FRAME FUNC GREATER GREATEREQ ID INT LESS LESSEQ LOAD MAIN MINUS OPBRACE OPBRACKET OPPARENTH PLUS PROGRAM READ RETURN THEN TIMES UNEQUAL VAR VOID WHEN WHILE WRITEprogram : encabezamiento var_list calcula_globales func_list cuerpo\n               | encabezamiento var_list calcula_globales cuerpo\n               | encabezamiento func_list cuerpo\n               | encabezamiento cuerpo\n    calcula_globales :\n    encabezamiento : PROGRAM ID\n    context_to_global : cuerpo : MAIN context_to_global OPPARENTH CLPARENTH OPBRACE estat_list CLBRACE\n    variable : VAR ID COLON var_typ\n                | VAR ID COLON var_typ dims\n    var_list : variable var_list\n                | variable\n    func_list : func func_list\n                 | func\n    estat_list : estat estat_list\n                  | estat\n    param_list : param COMMA param_list \n                  | param\n    save_array_size : \n    dims : OPBRACKET aritm save_array_size CLBRACKET\n            | OPBRACKET aritm save_array_size CLBRACKET OPBRACKET aritm save_array_size CLBRACKET\n    func : FUNC context_to_local ID OPPARENTH CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE\n            | FUNC context_to_local ID OPPARENTH param_list CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE\n    context_to_local :ciclo : WHILE OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE\n    decision : WHEN OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE\n               | WHEN OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE OPBRACE estat_list CLBRACE\n    func_cont : var_list estat_list RETURN aritm\n                 | estat_list RETURN aritm\n                 | var_list estat_list\n                 | estat_list\n    estat : asign\n             | llam_void\n             | lectura\n             | escritura\n             | carga_dt\n             | decision\n             | ciclo\n    carga_dt : ID ASGNMNT LOAD OPPARENTH ID CLPARENTH\n                | ID ASGNMNT LOAD OPPARENTH CONST_STRING CLPARENTH \n    param : ID COLON var_typ\n             | ID COLON var_typ dims\n    var_typ : INT\n               | FLOAT\n               | CHAR\n               | BOOL\n               | FRAME\n    func_typ : INT\n                | FLOAT\n                | CHAR\n                | BOOL\n                | FRAME\n                | VOID\n    check_aritm_operation :\n    check_aritm : \n    aritm : term check_aritm PLUS check_aritm_operation aritm\n             | term check_aritm MINUS check_aritm_operation aritm\n             | term check_aritm\n    check_term_operation :\n    check_term :\n    term : factor check_term TIMES check_term_operation term\n            | factor check_term DIVIDE check_term_operation term\n            | factor check_term\n    factortype_const_int : factortype_const_float : factor_const : CONST_INT factortype_const_int\n                    | CONST_FLOAT factortype_const_float\n    factor_var : ID\n                  | ID dims\n    factor_function_call : ID OPPARENTH CLPARENTH\n                              | ID OPPARENTH args CLPARENTH\n    factor : OPPARENTH aritm CLPARENTH\n              | factor_function_call\n              | factor_var\n              | factor_const\n    relac : aritm EQUAL aritm\n             | aritm UNEQUAL aritm\n             | aritm LESS aritm\n             | aritm LESSEQ aritm\n             | aritm GREATER aritm\n             | aritm GREATEREQ aritm\n    args : aritm COMMA args\n            | aritm\n    lectura : READ OPPARENTH CLPARENTH\n    escritura : WRITE OPPARENTH aritm CLPARENTH\n                 | WRITE OPPARENTH CONST_STRING CLPARENTH\n    llam_void : ID OPPARENTH CLPARENTH\n                 | ID OPPARENTH args CLPARENTH\n    asign : ID ASGNMNT lectura\n             | ID ASGNMNT aritm\n             | ID ASGNMNT CONST_STRING\n             | ID dims ASGNMNT lectura\n             | ID dims ASGNMNT aritm\n             | ID dims ASGNMNT CONST_STRING\n    '
    
_lr_action_items = {'PROGRAM':([0,],[3,]),'$end':([1,6,14,21,25,69,],[0,-4,-3,-2,-1,-8,]),'MAIN':([2,4,5,7,8,12,13,15,16,20,27,28,29,30,31,32,35,110,163,174,177,],[9,-5,9,-12,-14,-6,9,-11,-13,9,-9,-43,-44,-45,-46,-47,-10,-20,-22,-23,-21,]),'VAR':([2,7,12,27,28,29,30,31,32,35,110,119,146,177,],[10,10,-6,-9,-43,-44,-45,-46,-47,-10,-20,10,10,-21,]),'FUNC':([2,4,7,8,12,13,15,27,28,29,30,31,32,35,110,163,174,177,],[11,-5,-12,11,-6,11,-11,-9,-43,-44,-45,-46,-47,-10,-20,-22,-23,-21,]),'ID':([3,7,10,11,15,19,27,28,29,30,31,32,33,34,35,36,42,43,44,45,46,47,48,49,56,57,58,59,60,61,62,63,64,68,71,73,75,76,77,79,80,82,83,84,85,96,97,98,100,101,104,110,111,112,113,114,115,116,119,121,122,123,124,125,126,127,128,130,131,132,133,134,135,137,138,139,140,141,142,144,146,159,160,161,162,165,167,168,169,170,172,177,179,180,182,184,],[12,-12,18,-24,-11,24,-9,-43,-44,-45,-46,-47,37,50,-10,62,50,-32,-33,-34,-35,-36,-37,-38,-55,-60,62,-73,-74,-75,-68,-64,-65,37,62,62,62,62,62,-58,-63,62,-69,-66,-67,-89,-90,-91,62,-87,-84,-20,-54,-54,-59,-59,-72,-70,50,147,-92,-93,-94,-88,62,-85,-86,62,62,62,62,62,62,62,62,62,62,62,-71,50,50,-56,-57,-61,-62,62,-39,-40,50,50,62,-21,-26,-25,50,-27,]),'READ':([7,15,27,28,29,30,31,32,34,35,42,43,44,45,46,47,48,49,56,57,59,60,61,62,63,64,71,79,80,83,84,85,96,97,98,100,101,104,110,115,116,119,122,123,124,125,127,128,142,144,146,159,160,161,162,167,168,169,170,177,179,180,182,184,],[-12,-11,-9,-43,-44,-45,-46,-47,51,-10,51,-32,-33,-34,-35,-36,-37,-38,-55,-60,-73,-74,-75,-68,-64,-65,51,-58,-63,-69,-66,-67,-89,-90,-91,51,-87,-84,-20,-72,-70,51,-92,-93,-94,-88,-85,-86,-71,51,51,-56,-57,-61,-62,-39,-40,51,51,-21,-26,-25,51,-27,]),'WRITE':([7,15,27,28,29,30,31,32,34,35,42,43,44,45,46,47,48,49,56,57,59,60,61,62,63,64,79,80,83,84,85,96,97,98,101,104,110,115,116,119,122,123,124,125,127,128,142,144,146,159,160,161,162,167,168,169,170,177,179,180,182,184,],[-12,-11,-9,-43,-44,-45,-46,-47,52,-10,52,-32,-33,-34,-35,-36,-37,-38,-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,-89,-90,-91,-87,-84,-20,-72,-70,52,-92,-93,-94,-88,-85,-86,-71,52,52,-56,-57,-61,-62,-39,-40,52,52,-21,-26,-25,52,-27,]),'WHEN':([7,15,27,28,29,30,31,32,34,35,42,43,44,45,46,47,48,49,56,57,59,60,61,62,63,64,79,80,83,84,85,96,97,98,101,104,110,115,116,119,122,123,124,125,127,128,142,144,146,159,160,161,162,167,168,169,170,177,179,180,182,184,],[-12,-11,-9,-43,-44,-45,-46,-47,53,-10,53,-32,-33,-34,-35,-36,-37,-38,-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,-89,-90,-91,-87,-84,-20,-72,-70,53,-92,-93,-94,-88,-85,-86,-71,53,53,-56,-57,-61,-62,-39,-40,53,53,-21,-26,-25,53,-27,]),'WHILE':([7,15,27,28,29,30,31,32,34,35,42,43,44,45,46,47,48,49,56,57,59,60,61,62,63,64,79,80,83,84,85,96,97,98,101,104,110,115,116,119,122,123,124,125,127,128,142,144,146,159,160,161,162,167,168,169,170,177,179,180,182,184,],[-12,-11,-9,-43,-44,-45,-46,-47,54,-10,54,-32,-33,-34,-35,-36,-37,-38,-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,-89,-90,-91,-87,-84,-20,-72,-70,54,-92,-93,-94,-88,-85,-86,-71,54,54,-56,-57,-61,-62,-39,-40,54,54,-21,-26,-25,54,-27,]),'OPPARENTH':([9,17,24,36,50,51,52,53,54,58,62,71,73,75,76,77,82,99,100,111,112,113,114,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[-7,22,33,58,73,74,75,76,77,58,82,58,58,58,58,58,58,121,58,-54,-54,-59,-59,58,58,58,58,58,58,58,58,58,58,58,58,58,58,]),'COLON':([18,37,38,67,],[23,65,66,94,]),'CLPARENTH':([22,28,29,30,31,32,33,39,40,56,57,59,60,61,62,63,64,73,74,79,80,81,82,83,84,85,86,95,102,103,105,106,107,109,110,115,116,117,118,142,147,148,149,151,152,153,154,155,156,159,160,161,162,177,],[26,-43,-44,-45,-46,-47,38,67,-18,-55,-60,-73,-74,-75,-68,-64,-65,101,104,-58,-63,115,116,-69,-66,-67,-41,-17,125,-83,127,128,129,136,-20,-72,-70,142,-42,-71,167,168,-82,-76,-77,-78,-79,-80,-81,-56,-57,-61,-62,-21,]),'INT':([23,65,66,94,],[28,28,88,88,]),'FLOAT':([23,65,66,94,],[29,29,89,89,]),'CHAR':([23,65,66,94,],[30,30,90,90,]),'BOOL':([23,65,66,94,],[31,31,91,91,]),'FRAME':([23,65,66,94,],[32,32,92,92,]),'OPBRACE':([26,87,88,89,90,91,92,93,120,150,157,181,],[34,119,-48,-49,-50,-51,-52,-53,146,169,170,182,]),'OPBRACKET':([27,28,29,30,31,32,50,62,86,110,],[36,-43,-44,-45,-46,-47,36,36,36,137,]),'COMMA':([28,29,30,31,32,40,56,57,59,60,61,62,63,64,79,80,83,84,85,86,103,110,115,116,118,142,159,160,161,162,177,],[-43,-44,-45,-46,-47,68,-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,-41,126,-20,-72,-70,-42,-71,-56,-57,-61,-62,-21,]),'CONST_INT':([36,58,71,73,75,76,77,82,100,111,112,113,114,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[63,63,63,63,63,63,63,63,63,-54,-54,-59,-59,63,63,63,63,63,63,63,63,63,63,63,63,63,63,]),'CONST_FLOAT':([36,58,71,73,75,76,77,82,100,111,112,113,114,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[64,64,64,64,64,64,64,64,64,-54,-54,-59,-59,64,64,64,64,64,64,64,64,64,64,64,64,64,64,]),'CLBRACE':([41,42,43,44,45,46,47,48,49,56,57,59,60,61,62,63,64,70,79,80,83,84,85,96,97,98,101,104,110,115,116,122,123,124,125,127,128,142,143,145,159,160,161,162,164,166,167,168,173,175,176,177,178,179,180,183,184,],[69,-16,-32,-33,-34,-35,-36,-37,-38,-55,-60,-73,-74,-75,-68,-64,-65,-15,-58,-63,-69,-66,-67,-89,-90,-91,-87,-84,-20,-72,-70,-92,-93,-94,-88,-85,-86,-71,163,-31,-56,-57,-61,-62,-30,174,-39,-40,-29,179,180,-21,-28,-26,-25,184,-27,]),'RETURN':([42,43,44,45,46,47,48,49,56,57,59,60,61,62,63,64,70,79,80,83,84,85,96,97,98,101,104,110,115,116,122,123,124,125,127,128,142,145,159,160,161,162,164,167,168,177,179,180,184,],[-16,-32,-33,-34,-35,-36,-37,-38,-55,-60,-73,-74,-75,-68,-64,-65,-15,-58,-63,-69,-66,-67,-89,-90,-91,-87,-84,-20,-72,-70,-92,-93,-94,-88,-85,-86,-71,165,-56,-57,-61,-62,172,-39,-40,-21,-26,-25,-27,]),'ASGNMNT':([50,72,110,177,],[71,100,-20,-21,]),'CLBRACKET':([55,56,57,59,60,61,62,63,64,78,79,80,83,84,85,110,115,116,142,158,159,160,161,162,171,177,],[-19,-55,-60,-73,-74,-75,-68,-64,-65,110,-58,-63,-69,-66,-67,-20,-72,-70,-71,-19,-56,-57,-61,-62,177,-21,]),'PLUS':([56,57,59,60,61,62,63,64,79,80,83,84,85,110,115,116,142,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,111,-63,-69,-66,-67,-20,-72,-70,-71,-61,-62,-21,]),'MINUS':([56,57,59,60,61,62,63,64,79,80,83,84,85,110,115,116,142,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,112,-63,-69,-66,-67,-20,-72,-70,-71,-61,-62,-21,]),'EQUAL':([56,57,59,60,61,62,63,64,79,80,83,84,85,108,110,115,116,142,159,160,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,130,-20,-72,-70,-71,-56,-57,-61,-62,-21,]),'UNEQUAL':([56,57,59,60,61,62,63,64,79,80,83,84,85,108,110,115,116,142,159,160,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,131,-20,-72,-70,-71,-56,-57,-61,-62,-21,]),'LESS':([56,57,59,60,61,62,63,64,79,80,83,84,85,108,110,115,116,142,159,160,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,132,-20,-72,-70,-71,-56,-57,-61,-62,-21,]),'LESSEQ':([56,57,59,60,61,62,63,64,79,80,83,84,85,108,110,115,116,142,159,160,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,133,-20,-72,-70,-71,-56,-57,-61,-62,-21,]),'GREATER':([56,57,59,60,61,62,63,64,79,80,83,84,85,108,110,115,116,142,159,160,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,134,-20,-72,-70,-71,-56,-57,-61,-62,-21,]),'GREATEREQ':([56,57,59,60,61,62,63,64,79,80,83,84,85,108,110,115,116,142,159,160,161,162,177,],[-55,-60,-73,-74,-75,-68,-64,-65,-58,-63,-69,-66,-67,135,-20,-72,-70,-71,-56,-57,-61,-62,-21,]),'TIMES':([57,59,60,61,62,63,64,80,83,84,85,110,115,116,142,177,],[-60,-73,-74,-75,-68,-64,-65,113,-69,-66,-67,-20,-72,-70,-71,-21,]),'DIVIDE':([57,59,60,61,62,63,64,80,83,84,85,110,115,116,142,177,],[-60,-73,-74,-75,-68,-64,-65,114,-69,-66,-67,-20,-72,-70,-71,-21,]),'VOID':([66,94,],[93,93,]),'CONST_STRING':([71,75,100,121,],[98,106,124,148,]),'LOAD':([71,],[99,]),'THEN':([129,136,],[150,157,]),'ELSE':([179,],[181,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'encabezamiento':([0,],[2,]),'var_list':([2,7,119,146,],[4,15,144,144,]),'func_list':([2,8,13,],[5,16,20,]),'cuerpo':([2,5,13,20,],[6,14,21,25,]),'variable':([2,7,119,146,],[7,7,7,7,]),'func':([2,8,13,],[8,8,8,]),'calcula_globales':([4,],[13,]),'context_to_global':([9,],[17,]),'context_to_local':([11,],[19,]),'var_typ':([23,65,],[27,86,]),'dims':([27,50,62,86,],[35,72,83,118,]),'param_list':([33,68,],[39,95,]),'param':([33,68,],[40,40,]),'estat_list':([34,42,119,144,146,169,170,182,],[41,70,145,164,145,175,176,183,]),'estat':([34,42,119,144,146,169,170,182,],[42,42,42,42,42,42,42,42,]),'asign':([34,42,119,144,146,169,170,182,],[43,43,43,43,43,43,43,43,]),'llam_void':([34,42,119,144,146,169,170,182,],[44,44,44,44,44,44,44,44,]),'lectura':([34,42,71,100,119,144,146,169,170,182,],[45,45,96,122,45,45,45,45,45,45,]),'escritura':([34,42,119,144,146,169,170,182,],[46,46,46,46,46,46,46,46,]),'carga_dt':([34,42,119,144,146,169,170,182,],[47,47,47,47,47,47,47,47,]),'decision':([34,42,119,144,146,169,170,182,],[48,48,48,48,48,48,48,48,]),'ciclo':([34,42,119,144,146,169,170,182,],[49,49,49,49,49,49,49,49,]),'aritm':([36,58,71,73,75,76,77,82,100,126,130,131,132,133,134,135,137,138,139,165,172,],[55,81,97,103,105,108,108,103,123,103,151,152,153,154,155,156,158,159,160,173,178,]),'term':([36,58,71,73,75,76,77,82,100,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,161,162,56,56,]),'factor':([36,58,71,73,75,76,77,82,100,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'factor_function_call':([36,58,71,73,75,76,77,82,100,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,]),'factor_var':([36,58,71,73,75,76,77,82,100,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'factor_const':([36,58,71,73,75,76,77,82,100,126,130,131,132,133,134,135,137,138,139,140,141,165,172,],[61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,]),'save_array_size':([55,158,],[78,171,]),'check_aritm':([56,],[79,]),'check_term':([57,],[80,]),'factortype_const_int':([63,],[84,]),'factortype_const_float':([64,],[85,]),'func_typ':([66,94,],[87,120,]),'args':([73,82,126,],[102,117,149,]),'relac':([76,77,],[107,109,]),'check_aritm_operation':([111,112,],[138,139,]),'check_term_operation':([113,114,],[140,141,]),'func_cont':([119,146,],[143,166,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> encabezamiento var_list calcula_globales func_list cuerpo','program',5,'p_start','grammar.py',15),
  ('program -> encabezamiento var_list calcula_globales cuerpo','program',4,'p_start','grammar.py',16),
  ('program -> encabezamiento func_list cuerpo','program',3,'p_start','grammar.py',17),
  ('program -> encabezamiento cuerpo','program',2,'p_start','grammar.py',18),
  ('calcula_globales -> <empty>','calcula_globales',0,'p_calcula_globales','grammar.py',25),
  ('encabezamiento -> PROGRAM ID','encabezamiento',2,'p_encabezamiento','grammar.py',34),
  ('context_to_global -> <empty>','context_to_global',0,'p_context_to_global','grammar.py',49),
  ('cuerpo -> MAIN context_to_global OPPARENTH CLPARENTH OPBRACE estat_list CLBRACE','cuerpo',7,'p_cuerpo','grammar.py',55),
  ('variable -> VAR ID COLON var_typ','variable',4,'p_variable','grammar.py',61),
  ('variable -> VAR ID COLON var_typ dims','variable',5,'p_variable','grammar.py',62),
  ('var_list -> variable var_list','var_list',2,'p_var_list','grammar.py',71),
  ('var_list -> variable','var_list',1,'p_var_list','grammar.py',72),
  ('func_list -> func func_list','func_list',2,'p_func_list','grammar.py',78),
  ('func_list -> func','func_list',1,'p_func_list','grammar.py',79),
  ('estat_list -> estat estat_list','estat_list',2,'p_estat_list','grammar.py',85),
  ('estat_list -> estat','estat_list',1,'p_estat_list','grammar.py',86),
  ('param_list -> param COMMA param_list','param_list',3,'p_param_list','grammar.py',92),
  ('param_list -> param','param_list',1,'p_param_list','grammar.py',93),
  ('save_array_size -> <empty>','save_array_size',0,'p_save_array_size','grammar.py',99),
  ('dims -> OPBRACKET aritm save_array_size CLBRACKET','dims',4,'p_dims','grammar.py',110),
  ('dims -> OPBRACKET aritm save_array_size CLBRACKET OPBRACKET aritm save_array_size CLBRACKET','dims',8,'p_dims','grammar.py',111),
  ('func -> FUNC context_to_local ID OPPARENTH CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE','func',10,'p_func','grammar.py',118),
  ('func -> FUNC context_to_local ID OPPARENTH param_list CLPARENTH COLON func_typ OPBRACE func_cont CLBRACE','func',11,'p_func','grammar.py',119),
  ('context_to_local -> <empty>','context_to_local',0,'p_context_to_local','grammar.py',139),
  ('ciclo -> WHILE OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE','ciclo',8,'p_ciclo','grammar.py',148),
  ('decision -> WHEN OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE','decision',8,'p_decision','grammar.py',155),
  ('decision -> WHEN OPPARENTH relac CLPARENTH THEN OPBRACE estat_list CLBRACE ELSE OPBRACE estat_list CLBRACE','decision',12,'p_decision','grammar.py',156),
  ('func_cont -> var_list estat_list RETURN aritm','func_cont',4,'p_func_cont','grammar.py',164),
  ('func_cont -> estat_list RETURN aritm','func_cont',3,'p_func_cont','grammar.py',165),
  ('func_cont -> var_list estat_list','func_cont',2,'p_func_cont','grammar.py',166),
  ('func_cont -> estat_list','func_cont',1,'p_func_cont','grammar.py',167),
  ('estat -> asign','estat',1,'p_estat','grammar.py',173),
  ('estat -> llam_void','estat',1,'p_estat','grammar.py',174),
  ('estat -> lectura','estat',1,'p_estat','grammar.py',175),
  ('estat -> escritura','estat',1,'p_estat','grammar.py',176),
  ('estat -> carga_dt','estat',1,'p_estat','grammar.py',177),
  ('estat -> decision','estat',1,'p_estat','grammar.py',178),
  ('estat -> ciclo','estat',1,'p_estat','grammar.py',179),
  ('carga_dt -> ID ASGNMNT LOAD OPPARENTH ID CLPARENTH','carga_dt',6,'p_carga_dt','grammar.py',185),
  ('carga_dt -> ID ASGNMNT LOAD OPPARENTH CONST_STRING CLPARENTH','carga_dt',6,'p_carga_dt','grammar.py',186),
  ('param -> ID COLON var_typ','param',3,'p_param','grammar.py',192),
  ('param -> ID COLON var_typ dims','param',4,'p_param','grammar.py',193),
  ('var_typ -> INT','var_typ',1,'p_var_typ','grammar.py',203),
  ('var_typ -> FLOAT','var_typ',1,'p_var_typ','grammar.py',204),
  ('var_typ -> CHAR','var_typ',1,'p_var_typ','grammar.py',205),
  ('var_typ -> BOOL','var_typ',1,'p_var_typ','grammar.py',206),
  ('var_typ -> FRAME','var_typ',1,'p_var_typ','grammar.py',207),
  ('func_typ -> INT','func_typ',1,'p_func_typ','grammar.py',214),
  ('func_typ -> FLOAT','func_typ',1,'p_func_typ','grammar.py',215),
  ('func_typ -> CHAR','func_typ',1,'p_func_typ','grammar.py',216),
  ('func_typ -> BOOL','func_typ',1,'p_func_typ','grammar.py',217),
  ('func_typ -> FRAME','func_typ',1,'p_func_typ','grammar.py',218),
  ('func_typ -> VOID','func_typ',1,'p_func_typ','grammar.py',219),
  ('check_aritm_operation -> <empty>','check_aritm_operation',0,'p_check_aritm_operation','grammar.py',226),
  ('check_aritm -> <empty>','check_aritm',0,'p_check_aritm','grammar.py',242),
  ('aritm -> term check_aritm PLUS check_aritm_operation aritm','aritm',5,'p_aritm','grammar.py',273),
  ('aritm -> term check_aritm MINUS check_aritm_operation aritm','aritm',5,'p_aritm','grammar.py',274),
  ('aritm -> term check_aritm','aritm',2,'p_aritm','grammar.py',275),
  ('check_term_operation -> <empty>','check_term_operation',0,'p_check_term_operation','grammar.py',281),
  ('check_term -> <empty>','check_term',0,'p_check_term','grammar.py',296),
  ('term -> factor check_term TIMES check_term_operation term','term',5,'p_term','grammar.py',327),
  ('term -> factor check_term DIVIDE check_term_operation term','term',5,'p_term','grammar.py',328),
  ('term -> factor check_term','term',2,'p_term','grammar.py',329),
  ('factortype_const_int -> <empty>','factortype_const_int',0,'p_factortype_const_int','grammar.py',335),
  ('factortype_const_float -> <empty>','factortype_const_float',0,'p_factortype_const_float','grammar.py',343),
  ('factor_const -> CONST_INT factortype_const_int','factor_const',2,'p_factor_const','grammar.py',351),
  ('factor_const -> CONST_FLOAT factortype_const_float','factor_const',2,'p_factor_const','grammar.py',352),
  ('factor_var -> ID','factor_var',1,'p_factor_var','grammar.py',361),
  ('factor_var -> ID dims','factor_var',2,'p_factor_var','grammar.py',362),
  ('factor_function_call -> ID OPPARENTH CLPARENTH','factor_function_call',3,'p_factor_function_call','grammar.py',395),
  ('factor_function_call -> ID OPPARENTH args CLPARENTH','factor_function_call',4,'p_factor_function_call','grammar.py',396),
  ('factor -> OPPARENTH aritm CLPARENTH','factor',3,'p_factor','grammar.py',402),
  ('factor -> factor_function_call','factor',1,'p_factor','grammar.py',403),
  ('factor -> factor_var','factor',1,'p_factor','grammar.py',404),
  ('factor -> factor_const','factor',1,'p_factor','grammar.py',405),
  ('relac -> aritm EQUAL aritm','relac',3,'p_relac','grammar.py',461),
  ('relac -> aritm UNEQUAL aritm','relac',3,'p_relac','grammar.py',462),
  ('relac -> aritm LESS aritm','relac',3,'p_relac','grammar.py',463),
  ('relac -> aritm LESSEQ aritm','relac',3,'p_relac','grammar.py',464),
  ('relac -> aritm GREATER aritm','relac',3,'p_relac','grammar.py',465),
  ('relac -> aritm GREATEREQ aritm','relac',3,'p_relac','grammar.py',466),
  ('args -> aritm COMMA args','args',3,'p_args','grammar.py',472),
  ('args -> aritm','args',1,'p_args','grammar.py',473),
  ('lectura -> READ OPPARENTH CLPARENTH','lectura',3,'p_lectura','grammar.py',479),
  ('escritura -> WRITE OPPARENTH aritm CLPARENTH','escritura',4,'p_escritura','grammar.py',485),
  ('escritura -> WRITE OPPARENTH CONST_STRING CLPARENTH','escritura',4,'p_escritura','grammar.py',486),
  ('llam_void -> ID OPPARENTH CLPARENTH','llam_void',3,'p_llam_void','grammar.py',492),
  ('llam_void -> ID OPPARENTH args CLPARENTH','llam_void',4,'p_llam_void','grammar.py',493),
  ('asign -> ID ASGNMNT lectura','asign',3,'p_asign','grammar.py',499),
  ('asign -> ID ASGNMNT aritm','asign',3,'p_asign','grammar.py',500),
  ('asign -> ID ASGNMNT CONST_STRING','asign',3,'p_asign','grammar.py',501),
  ('asign -> ID dims ASGNMNT lectura','asign',4,'p_asign','grammar.py',502),
  ('asign -> ID dims ASGNMNT aritm','asign',4,'p_asign','grammar.py',503),
  ('asign -> ID dims ASGNMNT CONST_STRING','asign',4,'p_asign','grammar.py',504),
]
