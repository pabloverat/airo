# memory_bases.py

# global memory bases
global_mem_bases = dict(
    # vars_bool=11_000,
    vars_char=12_000,
    vars_int=13_000,
    vars_float=14_000,
    vars_frame=15_000,
    temps_bool=111_000,
    temps_int=113_000,
    temps_float=114_000,
    temps_ptr=119_000,
)

# local memory bases
local_mem_bases = dict(
    vars_bool=1_000,
    vars_char=2_000,
    vars_int=3_000,
    vars_float=4_000,
    vars_frame=5_000,
    temps_bool=101_000,
    temps_int=103_000,
    temps_float=104_000,
    temps_ptr=109_000,
)

# consts bases
consts_mem_bases = dict(
    vars_int=23_000,
    vars_float=24_000,
    vars_string=25_000,
)