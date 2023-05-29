# output_formatter.py

class Output_Formatter:
    
    def __init__(self, cuads=None, dir_funcs=None, consts=None) -> None:
        self.cuads = "" if cuads is None else cuads
        self.dir_funcs = "" if dir_funcs is None else dir_funcs
        self.consts = "" if consts is None else consts
        
    def build_ovejota(self) -> None:
        out_str = ""
        separator = "\n-#-#-#-#-#-\n"
        out_str = "".join([
            self.cuads,
            separator,
            self.dir_funcs,
            separator,
            self.consts
        ])
        
        with open("./ovejota.obj", "w+") as f:
            f.write(out_str)