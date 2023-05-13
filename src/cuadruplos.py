# cuadruplo.py

class Cuadruplo:
    
    def __init__(self, idx=None, operation=None, leftOp=None, rightOp=None, result=None) -> None:
        self.idx = idx
        self.operation = operation
        self.leftOp = leftOp
        self.rightOp = rightOp
        self.result = result
    
    def set_values(self, idx=None, operation=None, leftOp=None, rightOp=None, result=None) -> None:
        self.idx = idx
        self.operation = operation
        self.leftOp = leftOp
        self.rightOp = rightOp
        self.result = result
        
    def print(self) -> None:
        print(f"{self.idx}\t" if self.idx else "None\t", end="")
        print(f"{self.operation}\t" if self.operation else "None\t", end="")
        print(f"{self.leftOp}\t" if self.leftOp else "None\t", end="")
        print(f"{self.rightOp}\t" if self.rightOp else "None\t", end="")
        print(f"{self.result}" if self.result else "None\t", end="")
        print("\n", end="")



class Cuadruplos:
    
    def __init__(self) -> None:
        self.cuadruplos = []
        self.pilaSaltos = ['$']
        self.pilaTipos = ['$']
        self.pilaOperandos = ['$']
        self.pilaOperadores = ['$']
        
            
    def add_cuadruplo(self, idx=None, operation=None, leftOp=None, rightOp=None, result=None) -> None:
        new_cuadruplo = Cuadruplo()
        idx = len(self.cuadruplos) if idx is None else idx
        print("adding cuad: ", idx)
        new_cuadruplo.set_values(idx=idx, operation=operation, leftOp=leftOp, rightOp=rightOp, result=result)
        self.cuadruplos = self.cuadruplos + [new_cuadruplo]
        
    def print(self) -> None:
        for cuad in self.cuadruplos:
            print(f"{cuad.idx}\t" if cuad.idx else "None\t", end="")
            print(f"{cuad.operation}\t" if cuad.operation else "None\t", end="")
            print(f"{cuad.leftOp}\t" if cuad.leftOp else "None\t", end="")
            print(f"{cuad.rightOp}\t" if cuad.rightOp else "None\t", end="")
            print(f"{cuad.result}" if cuad.result else "None\t", end="")
            print("\n", end="")