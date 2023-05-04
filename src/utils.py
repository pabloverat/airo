# utils.py

# función usada para leer el archivo a compilar
def read_file(fname: str) -> str:
    with open(fname) as f:
        return '\n'.join(line.rstrip() for line in f)
    
# función auxiliar para imprimir el árbol de sintaxis
def print_control(p, nonterminal: str, max_symbols: int):
    print(f"Parsed {nonterminal}  \t\t", end="")
    for i in range(1, max_symbols+1):
        try:
            print(f"{p[i]}", end="\t")
        except:
            pass
    print("")
    
# Función para imprimir tokens del código
def print_tokens(myLexer):
    print("tokens are:")
    while True:
        tok = myLexer.token()
        if not tok: 
            break      # No more input
        print(tok)

    print("terminé el scanning")
    print("")