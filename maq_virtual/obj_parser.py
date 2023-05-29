# obj_parser.py

import json

class Obj_Parser:
    
    def __init__(self, obj_dir="./ovejota.obj") -> None:
        self.obj_dir = obj_dir
        
    def parse(self, obj_dir="./ovejota.obj"):
        obj_dir = obj_dir if obj_dir is not None else self.obj_dir
        
        with open("./ovejota.obj", "r") as f:
            input_str = f.read()
            separator = "\n-#-#-#-#-#-\n"
            input_list = input_str.split(separator)
            
            self.cuads = json.loads(input_list[0])
            self.dir_funcs = json.loads(input_list[1])
            self.consts = json.loads(input_list[2])
            
        return self.cuads, self.dir_funcs, self.consts